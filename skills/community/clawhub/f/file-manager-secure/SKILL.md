# File Manager Secure

name: file-manager-secure
description: Safe file operations with validation, dry-run mode, and trash recovery. Alternative to dangerous rm/mv/cp commands.

---

# File Manager Secure

## Overview

Secure file management with data loss prevention:
- **Dry-run mode** — Preview all operations before execution
- **Trash/recycle** — Recoverable deletion instead of permanent rm
- **Path validation** — Prevent traversal attacks and forbidden paths
- **Batch confirmation** — Review file list before bulk operations
- **Operation logging** — Complete audit trail

## Security Model

### Layer 1: Path Sanitization
```python
def validate_path(path: str) -> Path:
    # Resolve to absolute
    full_path = Path(path).resolve()
    
    # Check forbidden patterns
    FORBIDDEN_PATTERNS = [
        r"\.\.",           # Parent directory traversal
        r"~/.ssh",
        r"~/.gnupg",
        r"~/.aws",
        r"~/.docker",
        r"~/.kube",
        r"\.env",
        r"secret",
        r"token",
        r"credential",
        r"/etc/passwd",
        r"/etc/shadow",
        r"C:\\Windows\\System32",
        r"REGISTRY\\",
    ]
    
    # Must be within workspace or explicit allowlist
    WORKSPACE = Path.home() / ".openclaw" / "workspace"
    ALLOWED_DIRS = [WORKSPACE, Path.home() / "Downloads", Path.home() / "Documents"]
    
    for allowed in ALLOWED_DIRS:
        try:
            full_path.relative_to(allowed)
            return full_path
        except ValueError:
            continue
    
    raise PermissionError(f"Path {path} is outside allowed directories")
```

### Layer 2: Operation Dry-Run
```python
@dataclass
class FileOperation:
    op: str  # 'copy', 'move', 'delete', 'rename'
    source: Path
    dest: Optional[Path]
    size: int
    confirm_required: bool

# All operations return preview first
operations = plan_operations(files, action='delete')
show_preview(operations)  # User reviews
execute_with_confirmation(operations)  # Only after OK
```

### Layer 3: Trash Recovery
```python
TRASH_DIR = WORKSPACE / ".trash"

def safe_delete(path: Path):
    # Move to trash with metadata
    trash_entry = TRASH_DIR / f"{timestamp}_{path.name}"
    metadata = {
        "original_path": str(path),
        "deleted_at": timestamp,
        "size": path.stat().st_size,
    }
    shutil.move(path, trash_entry)
    save_metadata(trash_entry, metadata)
    # Auto-cleanup after 30 days
```

### Layer 4: Bulk Protection
```python
MAX_BULK_OPERATIONS = 50  # Require confirmation above this
MAX_TOTAL_SIZE = 100 * 1024 * 1024  # 100MB limit

# For large operations, require explicit --force flag
```

## Capabilities

### 1. List Directory
```bash
# Safe ls with filters
file-secure list /path/to/dir --type *.csv --sort size --reverse
```

### 2. Search Files
```bash
# Content and name search
file-secure search "pattern" --in=/path --type=md --content  # Search in content
file-secure search "dataset*" --in=/path --type=csv            # Search by name
```

### 3. Copy Files (Dry-run first)
```bash
file-secure copy source.csv backup/          # Preview mode
file-secure copy source.csv backup/ --exec   # Execute after preview
file-secure copy *.csv backup/ --exec       # Bulk with confirmation
```

### 4. Move Files (Dry-run first)
```bash
file-secure move old/ processed/ --exec
file-secure move *.tmp trash/ --exec        # Safe to trash, recoverable
```

### 5. Delete Files → Trash (Recoverable)
```bash
file-secure delete old.csv                   # Move to trash
file-secure delete *.log --older-than=30d    # Delete old files
file-secure restore old.csv                  # Restore from trash
file-secure empty-trash                      # Permanent delete (with warning)
```

### 6. Analyze Directory
```bash
file-secure analyze datasets/               # Size by type, largest files
file-secure analyze datasets/ --duplicates  # Find duplicates
```

### 7. Backup/Restore
```bash
file-secure backup important.csv
file-secure restore important.csv.bak
```

## Workflow

### Safe Delete Process
1. **Scan** — Find matching files
2. **Preview** — Show list with sizes and total
3. **Confirm** — User reviews and approves
4. **Trash** — Move to recoverable trash
5. **Log** — Record operation
6. **Verify** — Confirm files moved

### Safe Copy/Move Process
1. **Dry-run** — Show source → dest mapping
2. **Conflict check** — Detect overwrites
3. **Confirm** — User approves
4. **Execute** — Perform operations
5. **Verify** — Check results

## Resources

### scripts/
- `file_manager.py` — Main operations with safety layers
- `path_validator.py` — Path sanitization
- `trash_manager.py` — Trash operations and recovery
- `operation_planner.py` — Dry-run and batch planning

### references/
- `security_model.md` — Complete security architecture
- `recovery_guide.md` — How to restore deleted files

