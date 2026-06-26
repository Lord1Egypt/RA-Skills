#!/usr/bin/env python3
"""
Secure File Manager
Data-loss-prevention file operations with dry-run and trash recovery.
"""

import os
import re
import sys
import json
import shutil
import hashlib
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import List, Optional, Tuple
import fnmatch

# ============== CONFIGURATION ==============

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.home() / ".openclaw" / "workspace"))
TRASH_DIR = WORKSPACE / ".trash"
BACKUP_DIR = WORKSPACE / ".backups"
LOG_FILE = WORKSPACE / "memory" / "file_operations.log"

ALLOWED_DIRS = [WORKSPACE]
MAX_BULK_OPERATIONS = 50
MAX_TOTAL_SIZE_MB = 100

FORBIDDEN_PATTERNS = [
    r"\.\.", r"\.ssh", r"\.gnupg", r"\.aws", r"\.docker", r"\.kube",
    r"\.env", r"secret", r"token", r"credential", r"password",
    r"/etc/shadow", r"/etc/passwd", r"System32", r"REGISTRY"
]

# ============== DATA CLASSES ==============

@dataclass
class FileOperation:
    op: str
    source: str
    dest: Optional[str]
    size: int
    confirm_required: bool = True
    
    def to_dict(self):
        return asdict(self)

# ============== PATH VALIDATION ==============

def validate_path(path: str, must_exist: bool = True) -> Tuple[Path, str]:
    """Validate and sanitize a path."""
    try:
        # Expand and resolve
        expanded = os.path.expanduser(path)
        full_path = Path(expanded).resolve()
        
        # Check forbidden patterns
        path_str = str(full_path)
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, path_str, re.IGNORECASE):
                return None, f"FORBIDDEN: Path matches blocked pattern '{pattern}'"
        
        # Check allowed directories
        in_allowed = False
        for allowed in ALLOWED_DIRS:
            try:
                full_path.relative_to(allowed)
                in_allowed = True
                break
            except ValueError:
                continue
        
        if not in_allowed:
            return None, f"OUTSIDE_WORKSPACE: Path '{path}' is outside allowed directories"
        
        if must_exist and not full_path.exists():
            return None, f"NOT_FOUND: Path '{path}' does not exist"
        
        return full_path, "OK"
        
    except Exception as e:
        return None, f"ERROR: {e}"

# ============== LOGGING ==============

def log_operation(operation: str, source: str, dest: str = None, status: str = "OK"):
    """Log file operations for audit."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] {operation} | src={source} | dest={dest} | status={status}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

# ============== TRASH MANAGEMENT ==============

def move_to_trash(path: Path) -> Tuple[bool, str]:
    """Move file to trash with metadata for recovery."""
    try:
        TRASH_DIR.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = f"{timestamp}_{path.name}"
        trash_path = TRASH_DIR / safe_name
        
        # Handle duplicates
        counter = 1
        original_trash_path = trash_path
        while trash_path.exists():
            trash_path = TRASH_DIR / f"{safe_name}_{counter}"
            counter += 1
        
        # Move to trash
        shutil.move(str(path), str(trash_path))
        
        # Save metadata
        metadata = {
            "original_path": str(path),
            "trash_path": str(trash_path),
            "deleted_at": timestamp,
            "size": trash_path.stat().st_size if trash_path.is_file() else 0,
        }
        meta_file = trash_path.with_suffix(trash_path.suffix + ".trashmeta")
        with open(meta_file, "w") as f:
            json.dump(metadata, f, indent=2)
        
        log_operation("DELETE_TO_TRASH", str(path), str(trash_path))
        return True, f"Moved to trash: {trash_path.name}"
        
    except Exception as e:
        return False, f"TRASH_ERROR: {e}"

def restore_from_trash(filename: str) -> Tuple[bool, str]:
    """Restore a file from trash to original location."""
    try:
        # Find in trash
        matches = list(TRASH_DIR.glob(f"*_{filename}"))
        if not matches:
            return False, f"Not found in trash: {filename}"
        
        # Get most recent
        trash_path = sorted(matches, key=lambda p: p.stat().st_mtime, reverse=True)[0]
        meta_file = trash_path.with_suffix(trash_path.suffix + ".trashmeta")
        
        # Read metadata
        if meta_file.exists():
            with open(meta_file) as f:
                metadata = json.load(f)
            original_path = Path(metadata["original_path"])
        else:
            # Fallback: restore to workspace root
            original_path = WORKSPACE / filename
        
        # Ensure parent exists
        original_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Restore
        shutil.move(str(trash_path), str(original_path))
        if meta_file.exists():
            meta_file.unlink()
        
        log_operation("RESTORE_FROM_TRASH", str(trash_path), str(original_path))
        return True, f"Restored to: {original_path}"
        
    except Exception as e:
        return False, f"RESTORE_ERROR: {e}"

# ============== LIST OPERATIONS ==============

def list_directory(path: str, pattern: str = "*", sort_by: str = "name") -> Tuple[bool, List[dict], str]:
    """List directory contents with filters."""
    dir_path, error = validate_path(path)
    if error:
        return False, [], error
    
    try:
        items = []
        for item in dir_path.iterdir():
            if fnmatch.fnmatch(item.name, pattern):
                stat = item.stat()
                items.append({
                    "name": item.name,
                    "type": "dir" if item.is_dir() else "file",
                    "size": stat.st_size if item.is_file() else 0,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "path": str(item.relative_to(WORKSPACE))
                })
        
        # Sort
        if sort_by == "size":
            items.sort(key=lambda x: x["size"], reverse=True)
        elif sort_by == "modified":
            items.sort(key=lambda x: x["modified"], reverse=True)
        else:
            items.sort(key=lambda x: x["name"])
        
        return True, items, f"Found {len(items)} items"
        
    except Exception as e:
        return False, [], f"LIST_ERROR: {e}"

# ============== SEARCH OPERATIONS ==============

def search_files(path: str, pattern: str, in_content: bool = False) -> Tuple[bool, List[dict], str]:
    """Search files by name or content."""
    search_path, error = validate_path(path)
    if error:
        return False, [], error
    
    matches = []
    try:
        for root, dirs, files in os.walk(search_path):
            for filename in files:
                filepath = Path(root) / filename
                relative = str(filepath.relative_to(WORKSPACE))
                
                # Name match
                if fnmatch.fnmatch(filename, pattern) or pattern in filename:
                    matches.append({
                        "name": filename,
                        "path": relative,
                        "type": "name_match"
                    })
                
                # Content match (limited to text files)
                elif in_content and filepath.is_file():
                    if filepath.stat().st_size < 1024 * 1024:  # Max 1MB
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                if pattern in content:
                                    matches.append({
                                        "name": filename,
                                        "path": relative,
                                        "type": "content_match"
                                    })
                        except:
                            pass
        
        return True, matches, f"Found {len(matches)} matches"
        
    except Exception as e:
        return False, [], f"SEARCH_ERROR: {e}"

# ============== DELETE OPERATIONS ==============

def plan_delete(path: str, recursive: bool = False) -> Tuple[bool, List[FileOperation], str]:
    """Plan delete operations (dry-run)."""
    target_path, error = validate_path(path)
    if error:
        return False, [], error
    
    operations = []
    try:
        if target_path.is_file():
            operations.append(FileOperation(
                op="delete",
                source=str(target_path),
                dest=None,
                size=target_path.stat().st_size,
                confirm_required=True
            ))
        elif target_path.is_dir() and recursive:
            for item in target_path.rglob("*"):
                if item.is_file():
                    operations.append(FileOperation(
                        op="delete",
                        source=str(item),
                        dest=None,
                        size=item.stat().st_size,
                        confirm_required=True
                    ))
        
        total_size = sum(op.size for op in operations)
        msg = f"Plan: Delete {len(operations)} files ({total_size / 1024 / 1024:.2f} MB)"
        return True, operations, msg
        
    except Exception as e:
        return False, [], f"PLAN_ERROR: {e}"

def execute_delete(operations: List[FileOperation]) -> Tuple[bool, List[str]]:
    """Execute delete operations (move to trash)."""
    results = []
    for op in operations:
        success, msg = move_to_trash(Path(op.source))
        results.append(f"{'✓' if success else '✗'} {op.source}: {msg}")
    return True, results

# ============== COPY/MOVE OPERATIONS ==============

def plan_copy_move(source: str, dest: str, operation: str = "copy") -> Tuple[bool, List[FileOperation], str]:
    """Plan copy/move operations."""
    src_path, error = validate_path(source)
    if error:
        return False, [], error
    
    dest_path, error = validate_path(dest, must_exist=False)
    if error:
        return False, [], error
    
    operations = []
    try:
        if src_path.is_file():
            operations.append(FileOperation(
                op=operation,
                source=str(src_path),
                dest=str(dest_path / src_path.name) if dest_path.is_dir() else str(dest_path),
                size=src_path.stat().st_size,
                confirm_required=True
            ))
        elif src_path.is_dir():
            for item in src_path.rglob("*"):
                if item.is_file():
                    rel_path = item.relative_to(src_path)
                    target = dest_path / rel_path
                    operations.append(FileOperation(
                        op=operation,
                        source=str(item),
                        dest=str(target),
                        size=item.stat().st_size,
                        confirm_required=True
                    ))
        
        return True, operations, f"Plan: {operation} {len(operations)} files"
        
    except Exception as e:
        return False, [], f"PLAN_ERROR: {e}"

def execute_copy_move(operations: List[FileOperation]) -> Tuple[bool, List[str]]:
    """Execute copy/move operations."""
    results = []
    for op in operations:
        try:
            src = Path(op.source)
            dst = Path(op.dest)
            dst.parent.mkdir(parents=True, exist_ok=True)
            
            if op.op == "copy":
                shutil.copy2(str(src), str(dst))
                log_operation("COPY", str(src), str(dst))
            else:
                shutil.move(str(src), str(dst))
                log_operation("MOVE", str(src), str(dst))
            
            results.append(f"✓ {op.op}: {src.name} -> {dst}")
        except Exception as e:
            results.append(f"✗ {op.op} failed: {src.name} - {e}")
    
    return True, results

# ============== MAIN ==============

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command provided"}, indent=2))
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    # LIST
    if cmd == "list":
        path = sys.argv[2] if len(sys.argv) > 2 else "."
        pattern = sys.argv[3] if len(sys.argv) > 3 else "*"
        success, items, msg = list_directory(path, pattern)
        print(json.dumps({"success": success, "items": items, "message": msg}, indent=2))
    
    # SEARCH
    elif cmd == "search":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Pattern required"}, indent=2))
            sys.exit(1)
        pattern = sys.argv[2]
        path = sys.argv[3] if len(sys.argv) > 3 else "."
        in_content = "--content" in sys.argv
        success, matches, msg = search_files(path, pattern, in_content)
        print(json.dumps({"success": success, "matches": matches, "message": msg}, indent=2))
    
    # DELETE (plan)
    elif cmd == "delete":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Path required"}, indent=2))
            sys.exit(1)
        path = sys.argv[2]
        recursive = "--recursive" in sys.argv
        success, operations, msg = plan_delete(path, recursive)
        print(json.dumps({
            "success": success,
            "operations": [op.to_dict() for op in operations],
            "message": msg,
            "requires_confirmation": True
        }, indent=2))
    
    # DELETE (execute)
    elif cmd == "delete-confirm":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Operations JSON required"}, indent=2))
            sys.exit(1)
        try:
            ops_data = json.loads(sys.argv[2])
            operations = [FileOperation(**op) for op in ops_data]
            success, results = execute_delete(operations)
            print(json.dumps({"success": success, "results": results}, indent=2))
        except Exception as e:
            print(json.dumps({"error": f"Invalid operations data: {e}"}, indent=2))
    
    # RESTORE
    elif cmd == "restore":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Filename required"}, indent=2))
            sys.exit(1)
        filename = sys.argv[2]
        success, msg = restore_from_trash(filename)
        print(json.dumps({"success": success, "message": msg}, indent=2))
    
    else:
        print(json.dumps({"error": f"Unknown command: {cmd}"}, indent=2))

if __name__ == "__main__":
    main()
