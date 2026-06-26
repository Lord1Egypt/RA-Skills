#!/bin/bash
#
# CtrlZ - AI Operation Undo System
# Record and revert all changes made by AI
#

set -e

DB_PATH="${CTRLZ_DB:-$HOME/.openclaw/skills/ctrlz/undo.db}"
MAX_STACK="${CTRLZ_STACK_SIZE:-1}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Initialize database
init_db() {
  mkdir -p "$(dirname "$DB_PATH")"
  sqlite3 "$DB_PATH" << 'EOF'
-- Undo unit (one per conversation round)
CREATE TABLE IF NOT EXISTS undo_sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_key TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  description TEXT,
  status TEXT DEFAULT 'active' -- active, undone, expired
);

-- Specific operation records
CREATE TABLE IF NOT EXISTS undo_operations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL,
  type TEXT NOT NULL, -- file_write, file_edit, file_delete, dir_create, exec_install, etc.
  target_path TEXT NOT NULL,
  backup_path TEXT, -- Backup file path (if applicable)
  original_content BLOB, -- Original content (for text files)
  metadata TEXT, -- Additional info in JSON format
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (session_id) REFERENCES undo_sessions(id) ON DELETE CASCADE
);

-- Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_session_key ON undo_sessions(session_key);
CREATE INDEX IF NOT EXISTS idx_session_status ON undo_sessions(status);
CREATE INDEX IF NOT EXISTS idx_op_session ON undo_operations(session_id);

-- Settings table (stores stack size and other config)
CREATE TABLE IF NOT EXISTS settings (
  key TEXT PRIMARY KEY,
  value TEXT
);

-- Initialize default stack size
INSERT OR IGNORE INTO settings (key, value) VALUES ('max_stack_size', '1');
EOF
}

# Get setting
get_setting() {
  local key="$1"
  sqlite3 "$DB_PATH" "SELECT value FROM settings WHERE key = '$key';"
}

# Set setting
set_setting() {
  local key="$1"
  local value="$2"
  sqlite3 "$DB_PATH" "INSERT OR REPLACE INTO settings (key, value) VALUES ('$key', '$value');"
}

# Start a new undo session
start_session() {
  local session_key="$1"
  local description="${2:-}"
  
  # Cleanup old expired sessions (exceeding max_stack)
  cleanup_old_sessions
  
  # Create new session
  local session_id=$(sqlite3 "$DB_PATH" "INSERT INTO undo_sessions (session_key, description) VALUES ('$session_key', '$description'); SELECT last_insert_rowid();")
  echo "$session_id"
}

# Record file operation
record_operation() {
  local session_id="$1"
  local op_type="$2"
  local target_path="$3"
  local backup_path="${4:-}"
  local metadata="${5:-}"
  
  # If edit operation, try to read original content for backup
  local original_content=""
  if [[ "$op_type" == "file_edit" && -f "$target_path" ]]; then
    original_content=$(cat "$target_path" | base64 -w 0)
  fi
  
  # Escape special characters
  target_path=$(echo "$target_path" | sed "s/'/''/g")
  backup_path=$(echo "$backup_path" | sed "s/'/''/g")
  metadata=$(echo "$metadata" | sed "s/'/''/g")
  original_content=$(echo "$original_content" | sed "s/'/''/g")
  
  sqlite3 "$DB_PATH" << EOF
INSERT INTO undo_operations (session_id, type, target_path, backup_path, original_content, metadata)
VALUES ($session_id, '$op_type', '$target_path', '$backup_path', '$original_content', '$metadata');
EOF
}

# Cleanup old sessions (maintain stack size)
cleanup_old_sessions() {
  local max_size=$(get_setting 'max_stack_size')
  max_size="${max_size:-1}"
  
  # Keep recent N active sessions, mark others as expired
  sqlite3 "$DB_PATH" << EOF
UPDATE undo_sessions 
SET status = 'expired' 
WHERE id IN (
  SELECT id FROM undo_sessions 
  WHERE status = 'active' 
  ORDER BY created_at DESC 
  LIMIT -1 OFFSET $max_size
);

-- Delete operation records of expired sessions
DELETE FROM undo_operations 
WHERE session_id IN (
  SELECT id FROM undo_sessions WHERE status = 'expired'
);

-- Delete expired sessions
DELETE FROM undo_sessions WHERE status = 'expired';
EOF
}

# List undoable sessions
list_undoable() {
  local limit="${1:-10}"
  sqlite3 "$DB_PATH" << EOF
.headers on
.mode column
SELECT 
  id,
  datetime(created_at, 'localtime') as time,
  substr(description, 1, 50) as description,
  (SELECT COUNT(*) FROM undo_operations WHERE session_id = undo_sessions.id) as operations
FROM undo_sessions 
WHERE status = 'active' 
ORDER BY created_at DESC 
LIMIT $limit;
EOF
}

# Get session details
get_session_details() {
  local session_id="$1"
  sqlite3 "$DB_PATH" << EOF
SELECT 
  id,
  type,
  target_path,
  metadata
FROM undo_operations 
WHERE session_id = $session_id
ORDER BY id;
EOF
}

# Execute undo
undo() {
  local count="${1:-1}"
  local undone_count=0
  local packages_to_remove=()
  
  for i in $(seq 1 $count); do
    # Get latest active session
    local session_id=$(sqlite3 "$DB_PATH" "SELECT id FROM undo_sessions WHERE status = 'active' ORDER BY created_at DESC LIMIT 1;")
    
    if [[ -z "$session_id" ]]; then
      echo "{\"error\": \"No more operations to undo\", \"undone\": $undone_count}"
      return 1
    fi
    
    # Get all operations of this session
    local ops=$(sqlite3 "$DB_PATH" "SELECT type, target_path, backup_path, original_content FROM undo_operations WHERE session_id = $session_id ORDER BY id DESC;")
    
    # Execute undo for each operation
    while IFS='|' read -r op_type target_path backup_path original_content; do
      case "$op_type" in
        file_write|file_edit)
          if [[ -n "$backup_path" && -f "$backup_path" ]]; then
            cp "$backup_path" "$target_path"
          elif [[ -n "$original_content" ]]; then
            echo "$original_content" | base64 -d > "$target_path"
          else
            # If no backup, delete file
            rm -f "$target_path"
          fi
          ;;
        file_delete)
          # Restore deleted file (if backup exists)
          if [[ -n "$backup_path" && -f "$backup_path" ]]; then
            cp "$backup_path" "$target_path"
          fi
          ;;
        dir_create)
          # Delete created directory
          if [[ -d "$target_path" ]]; then
            rm -rf "$target_path"
          fi
          ;;
        exec_install|package_install)
          # Collect packages to remove, ask user later
          packages_to_remove+=("$target_path")
          ;;
      esac
    done <<< "$ops"
    
    # Mark session as undone
    sqlite3 "$DB_PATH" "UPDATE undo_sessions SET status = 'undone' WHERE id = $session_id;"
    undone_count=$((undone_count + 1))
  done
  
  # If package installations exist, list and ask user
  if [[ ${#packages_to_remove[@]} -gt 0 ]]; then
    echo "" >&2
    echo "📦 The following package installations cannot be auto-undone:" >&2
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >&2
    local idx=1
    for pkg in "${packages_to_remove[@]}"; do
      echo "  $idx. $pkg" >&2
      ((idx++))
    done
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >&2
    echo "" >&2
    echo "💡 To remove, manually execute:" >&2
    for pkg in "${packages_to_remove[@]}"; do
      # Parse package type
      if [[ "$pkg" == npm:* ]]; then
        echo "   npm uninstall ${pkg#npm:}" >&2
      elif [[ "$pkg" == pip:* ]]; then
        echo "   pip uninstall ${pkg#pip:}" >&2
      elif [[ "$pkg" == apt:* ]]; then
        echo "   sudo apt remove ${pkg#apt:}" >&2
      else
        echo "   # Package: $pkg" >&2
      fi
    done
    echo "" >&2
  fi
  
  echo "{\"undone\": $undone_count, \"message\": \"Successfully undone $undone_count operation(s)\"}"
}

# Show statistics
stats() {
  local active=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM undo_sessions WHERE status = 'active';")
  local total=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM undo_sessions;")
  local operations=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM undo_operations;")
  local max_stack=$(get_setting 'max_stack_size')
  
  echo "{\"active_sessions\": $active, \"total_sessions\": $total, \"total_operations\": $operations, \"max_stack_size\": $max_stack}"
}

# Backup file (call before modification)
backup_file() {
  local file_path="$1"
  local backup_dir="$HOME/.openclaw/skills/ctrlz/backups"
  mkdir -p "$backup_dir"
  
  if [[ -f "$file_path" ]]; then
    local backup_name="$(date +%s)_$(basename "$file_path" | tr '/' '_')"
    local backup_path="$backup_dir/$backup_name"
    cp "$file_path" "$backup_path"
    echo "$backup_path"
  else
    echo ""
  fi
}

# Clear all records
clear_all() {
  sqlite3 "$DB_PATH" "DELETE FROM undo_operations; DELETE FROM undo_sessions;"
  rm -rf "$HOME/.openclaw/skills/ctrlz/backups"
  echo "{\"cleared\": true}"
}

# CLI main program
main() {
  init_db
  
  local cmd="${1:-help}"
  shift || true
  
  case "$cmd" in
    init)
      # Initialize database (auto-executed)
      echo "{\"initialized\": true, \"db_path\": \"$DB_PATH\"}"
      ;;
      
    start)
      # Start new session
      local session_key="${1:-default}"
      local description="${2:-}"
      local session_id=$(start_session "$session_key" "$description")
      echo "{\"session_id\": $session_id, \"status\": \"started\"}"
      ;;
      
    record)
      # Record operation
      local session_id="$1"
      local op_type="$2"
      local target_path="$3"
      shift 3 || true
      local metadata="${*:-}"
      
      # Backup file (if file operation)
      local backup_path=""
      if [[ "$op_type" =~ ^file_ && -f "$target_path" ]]; then
        backup_path=$(backup_file "$target_path")
      fi
      
      record_operation "$session_id" "$op_type" "$target_path" "$backup_path" "$metadata"
      echo "{\"recorded\": true, \"type\": \"$op_type\", \"target\": \"$target_path\"}"
      ;;
      
    undo)
      # Undo operation
      local count="${1:-1}"
      undo "$count"
      ;;
      
    list)
      # List undoable sessions
      local limit="${1:-10}"
      list_undoable "$limit"
      ;;
      
    details)
      # Show session details
      local session_id="$1"
      get_session_details "$session_id"
      ;;
      
    set-stack)
      # Set stack size
      local size="${1:-1}"
      set_setting 'max_stack_size' "$size"
      echo "{\"max_stack_size\": $size}"
      ;;
      
    get-stack)
      # Get stack size
      local size=$(get_setting 'max_stack_size')
      echo "{\"max_stack_size\": ${size:-1}}"
      ;;
      
    stats)
      stats
      ;;
      
    clear)
      clear_all
      ;;
      
    help|*)
      cat << 'HELP'
CtrlZ - AI Operation Undo System

Usage: ctrlz <command> [args]

Commands:
  init                    Initialize database
  start <key> [desc]      Start new undo session
  record <sid> <type> <path> [metadata]  Record operation
  undo [count]            Undo recent N sessions (default 1)
  list [limit]            List undoable sessions
  details <session_id>    Show session details
  set-stack <size>        Set stack size (default 1)
  get-stack               Get current stack size
  stats                   Show statistics
  clear                   Clear all records

Environment Variables:
  CTRLZ_DB                Database path (default ~/.openclaw/skills/ctrlz/undo.db)
  CTRLZ_STACK_SIZE        Default stack size

Examples:
  ctrlz start my-session "Modify config file"
  ctrlz record 1 file_edit /path/to/config.json
  ctrlz undo
  ctrlz undo 3
  ctrlz list
  ctrlz set-stack 5
HELP
      ;;
  esac
}

main "$@"
