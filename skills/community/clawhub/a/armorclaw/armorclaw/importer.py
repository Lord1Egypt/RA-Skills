"""ArmorClaw — .env file importer."""
import os, shutil
from pathlib import Path
from datetime import datetime
from .store import set_secret


def parse_env_file(path: str) -> dict[str, str]:
    """Parse a .env file into a dict. Skips comments and empty lines."""
    result = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key   = key.strip()
            value = value.strip().strip('"').strip("'")
            if key:
                result[key] = value
    return result


def import_env_file(env_path: str, password: str,
                    skill: str = "importer",
                    confirm: bool = True) -> dict:
    """
    Import keys from a .env file into ArmorClaw.
    Returns: {imported: [...], skipped: [...], errors: [...]}
    """
    path = Path(env_path).expanduser().resolve()
    if not path.exists():
        return {"error": f"File not found: {path}"}

    keys = parse_env_file(str(path))
    if not keys:
        return {"error": "No keys found in .env file"}

    imported, skipped, errors = [], [], []

    for name, value in keys.items():
        if not value:
            skipped.append(name)
            continue
        try:
            set_secret(name, value, password, skill=skill)
            imported.append(name)
        except Exception as e:
            errors.append({"key": name, "error": str(e)})

    return {"imported": imported, "skipped": skipped, "errors": errors,
            "source": str(path)}


def handle_env_after_import(env_path: str, action: str) -> dict:
    """
    action: 'delete' | 'backup' | 'keep'
    Returns result dict.
    """
    path = Path(env_path).expanduser().resolve()
    if not path.exists():
        return {"ok": False, "error": "File not found"}

    if action == "delete":
        path.unlink()
        return {"ok": True, "action": "deleted", "path": str(path)}

    elif action == "backup":
        ts      = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup  = path.parent / f"{path.name}.backup-{ts}"
        shutil.copy2(str(path), str(backup))
        path.unlink()
        return {"ok": True, "action": "backup", "backup": str(backup), "original_deleted": True}

    else:  # keep
        return {"ok": True, "action": "kept", "path": str(path)}


def scan_for_env_files(search_paths: list[str] | None = None) -> list[str]:
    """Scan common locations for .env and secrets files."""
    defaults = [
        "~/.openclaw",
        "~/projects",
        "~/Documents",
    ]
    skip_dirs = {"node_modules", ".git", "venv", "__pycache__", "dist", "build"}
    found = []

    for base in (search_paths or defaults):
        p = Path(base).expanduser()
        if not p.exists():
            continue

        # Match .env files AND *.env files in .secrets/ folders
        for pattern in (".env", "*.env"):
            for env_file in p.rglob(pattern):
                parts = env_file.parts
                if any(x in parts for x in skip_dirs):
                    continue
                path_str = str(env_file)
                if path_str not in found:
                    found.append(path_str)

    return sorted(found)
