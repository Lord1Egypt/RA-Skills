#!/usr/bin/env python3
"""
Dynamic Skill Manager for OpenClaw

Manage skill lifecycle: install, track, cleanup.
"""

import json
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Data directory
DATA_DIR = Path.home() / ".openclaw" / "workspace" / ".skill-manager"
REGISTRY_FILE = DATA_DIR / "registry.json"
USAGE_LOG_FILE = DATA_DIR / "usage-log.jsonl"
ARCHIVE_DIR = DATA_DIR / "archive"
SKILLS_DIR = Path.home() / ".openclaw" / "workspace" / "skills"


def ensure_data_dir():
    """Ensure data directory and files exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    
    if not REGISTRY_FILE.exists():
        REGISTRY_FILE.write_text(json.dumps({"skills": {}}, indent=2))
    
    if not USAGE_LOG_FILE.exists():
        USAGE_LOG_FILE.touch()


def load_registry() -> dict:
    """Load skill registry."""
    ensure_data_dir()
    return json.loads(REGISTRY_FILE.read_text())


def save_registry(registry: dict):
    """Save skill registry."""
    REGISTRY_FILE.write_text(json.dumps(registry, indent=2))


# System skills that should never be removed
SYSTEM_SKILLS = {
    "self-improving-agent",  # Continuous learning
    "dynamic-skill-manager", # This skill itself
    "error-log-selfcheck",   # Error handling
    "pahf",                  # Personalization framework
}


def register_skill(skill_name: str, source: str = "clawhub", context_keywords: list = None, pinned: bool = None):
    """Register a newly installed skill."""
    registry = load_registry()
    
    # Auto-pin system skills
    if pinned is None:
        pinned = skill_name in SYSTEM_SKILLS
    
    if skill_name not in registry["skills"]:
        registry["skills"][skill_name] = {
            "installed_at": datetime.utcnow().isoformat() + "Z",
            "source": source,
            "usage_count": 0,
            "last_used": None,
            "context_keywords": context_keywords or [],
            "pinned": pinned  # Pinned skills are never removed by GC
        }
        save_registry(registry)
        return True
    return False


def track_usage(skill_name: str, context_summary: str, success: bool = True):
    """Record skill usage."""
    ensure_data_dir()
    
    # Update registry
    registry = load_registry()
    if skill_name in registry["skills"]:
        registry["skills"][skill_name]["usage_count"] += 1
        registry["skills"][skill_name]["last_used"] = datetime.utcnow().isoformat() + "Z"
        save_registry(registry)
    
    # Append to usage log
    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "skill": skill_name,
        "context": context_summary,
        "success": success
    }
    with open(USAGE_LOG_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")


def list_skills() -> dict:
    """List all tracked skills with their stats."""
    registry = load_registry()
    return registry["skills"]


def list_pinned_skills() -> list:
    """List pinned (system) skills."""
    registry = load_registry()
    return [name for name, data in registry["skills"].items() if data.get("pinned", False)]


def list_installed_skills() -> list:
    """List skills actually installed in skills directory."""
    if not SKILLS_DIR.exists():
        return []
    return [d.name for d in SKILLS_DIR.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]


def find_idle_skills(days: int = 30) -> list:
    """Find skills not used in N days (excluding pinned skills)."""
    registry = load_registry()
    cutoff = datetime.utcnow() - timedelta(days=days)
    
    idle_skills = []
    for skill_name, data in registry["skills"].items():
        # Skip pinned skills (system skills)
        if data.get("pinned", False):
            continue
        
        if data["last_used"]:
            last_used = datetime.fromisoformat(data["last_used"].rstrip("Z"))
            if last_used < cutoff:
                idle_skills.append({
                    "name": skill_name,
                    "last_used": data["last_used"],
                    "usage_count": data["usage_count"]
                })
        elif data["usage_count"] == 0:
            # Never used
            idle_skills.append({
                "name": skill_name,
                "last_used": None,
                "usage_count": 0
            })
    
    return idle_skills


def validate_skill_name(skill_name: str) -> bool:
    """Validate skill name to prevent path traversal attacks.
    
    Args:
        skill_name: The skill name to validate
        
    Returns:
        True if valid, False if contains dangerous patterns
    """
    # Reject empty names
    if not skill_name or not skill_name.strip():
        return False
    
    # Reject path separators and traversal patterns
    dangerous_patterns = ['/', '\\', '..', '\x00']
    for pattern in dangerous_patterns:
        if pattern in skill_name:
            return False
    
    # Reject absolute paths (starting with / or drive letter)
    if skill_name.startswith('/') or (len(skill_name) > 1 and skill_name[1] == ':'):
        return False
    
    # Skill name should be a simple directory name (alphanumeric, dash, underscore)
    import re
    if not re.match(r'^[a-zA-Z0-9_-]+$', skill_name):
        return False
    
    return True


def uninstall_skill(skill_name: str, archive: bool = True, force: bool = False) -> bool:
    """Uninstall a skill and optionally archive its metadata.
    
    SECURITY: This function validates skill_name to prevent path traversal attacks.
    Only safe skill names are allowed, and the resolved path is verified to be
    within the skills directory before any deletion occurs.
    
    Args:
        skill_name: Name of the skill to uninstall (must be safe directory name)
        archive: Whether to archive metadata before removal
        force: Skip confirmation (use with caution)
        
    Returns:
        True if successful, False if skill not found or validation failed
        
    Raises:
        ValueError: If skill_name is invalid or path traversal attempted
    """
    # Step 1: Validate skill name (prevent path traversal)
    if not validate_skill_name(skill_name):
        raise ValueError(
            f"Invalid skill name '{skill_name}'. "
            "Skill names must contain only alphanumeric characters, dashes, and underscores."
        )
    
    # Step 2: Resolve paths and verify containment
    skill_path = (SKILLS_DIR / skill_name).resolve()
    skills_dir_resolved = SKILLS_DIR.resolve()
    
    # Security check: ensure resolved path is within skills directory
    if not str(skill_path).startswith(str(skills_dir_resolved) + os.sep):
        raise ValueError(
            f"Security violation: skill path '{skill_path}' is outside skills directory. "
            "Path traversal attempt blocked."
        )
    
    # Step 3: Verify the path exists and is a directory
    if not skill_path.exists():
        return False
    
    if not skill_path.is_dir():
        raise ValueError(f"Skill path '{skill_path}' is not a directory")
    
    # Step 4: Additional symlink check (prevent symlink attacks)
    if skill_path.is_symlink():
        raise ValueError(
            f"Security violation: skill path '{skill_path}' is a symlink. "
            "Symlinks are not allowed for safety."
        )
    
    registry = load_registry()
    
    # Step 5: Prevent uninstalling system skills
    if skill_name in SYSTEM_SKILLS and not force:
        raise ValueError(
            f"Cannot uninstall system skill '{skill_name}'. "
            "System skills are protected. Use --force to override (not recommended)."
        )
    
    # Step 6: Archive metadata before removal
    if archive and skill_name in registry["skills"]:
        archive_file = ARCHIVE_DIR / f"{skill_name}.json"
        archive_data = registry["skills"][skill_name].copy()
        archive_data["uninstalled_at"] = datetime.utcnow().isoformat() + "Z"
        archive_file.write_text(json.dumps(archive_data, indent=2))
    
    # Step 7: Remove skill directory (now safe)
    shutil.rmtree(skill_path)
    
    # Step 8: Remove from registry
    if skill_name in registry["skills"]:
        del registry["skills"][skill_name]
        save_registry(registry)
    
    return True


def get_archived_skill(skill_name: str) -> Optional[dict]:
    """Get archived skill metadata for re-installation."""
    archive_file = ARCHIVE_DIR / f"{skill_name}.json"
    if archive_file.exists():
        return json.loads(archive_file.read_text())
    return None


def match_context_to_skill(context: str) -> list:
    """Match user context to skill keywords (simple keyword matching)."""
    registry = load_registry()
    context_lower = context.lower()
    
    matches = []
    for skill_name, data in registry["skills"].items():
        for keyword in data.get("context_keywords", []):
            if keyword.lower() in context_lower:
                matches.append({
                    "skill": skill_name,
                    "matched_keyword": keyword,
                    "usage_count": data["usage_count"]
                })
                break
    
    return sorted(matches, key=lambda x: x["usage_count"], reverse=True)


def sync_with_installed():
    """Sync registry with actually installed skills."""
    installed = set(list_installed_skills())
    registry = load_registry()
    tracked = set(registry["skills"].keys())
    
    # Add untracked skills
    for skill in installed - tracked:
        registry["skills"][skill] = {
            "installed_at": datetime.utcnow().isoformat() + "Z",
            "source": "unknown",
            "usage_count": 0,
            "last_used": None,
            "context_keywords": [],
            "pinned": skill in SYSTEM_SKILLS  # Auto-pin system skills
        }
    
    # Mark system skills as pinned if not already
    for skill in SYSTEM_SKILLS:
        if skill in registry["skills"]:
            registry["skills"][skill]["pinned"] = True
    
    # Remove tracked but not installed (skip if archived)
    for skill in tracked - installed:
        if skill in registry["skills"]:
            del registry["skills"][skill]
    
    save_registry(registry)
    return {"added": installed - tracked, "removed": tracked - installed}


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: skill_manager.py <command> [args]")
        print("Commands: list, pinned, idle <days>, sync, track <skill> <context>, uninstall <skill>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        skills = list_skills()
        for name, data in skills.items():
            pinned = "📌" if data.get("pinned", False) else " "
            print(f"{pinned} {name}: used {data['usage_count']}x, last: {data['last_used'] or 'never'}")
    
    elif cmd == "pinned":
        pinned = list_pinned_skills()
        print("Pinned (system) skills:")
        for name in pinned:
            print(f"  📌 {name}")
    
    elif cmd == "idle":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        idle = find_idle_skills(days)
        if not idle:
            print(f"No idle skills (all used within {days} days or pinned)")
        else:
            print(f"Idle skills (not used in {days} days):")
            for skill in idle:
                print(f"  {skill['name']}: last used {skill['last_used'] or 'never'}")
    
    elif cmd == "sync":
        result = sync_with_installed()
        print(f"Synced: Added {len(result['added'])}, Removed {len(result['removed'])}")
    
    elif cmd == "track":
        if len(sys.argv) < 4:
            print("Usage: track <skill> <context>")
            sys.exit(1)
        track_usage(sys.argv[2], sys.argv[3])
        print(f"Tracked usage of {sys.argv[2]}")
    
    elif cmd == "uninstall":
        if len(sys.argv) < 3:
            print("Usage: uninstall <skill>")
            print("WARNING: This will permanently delete the skill directory.")
            sys.exit(1)
        skill_name = sys.argv[2]
        try:
            result = uninstall_skill(skill_name)
            if result:
                print(f"✓ Successfully uninstalled '{skill_name}'")
            else:
                print(f"✗ Skill '{skill_name}' not found")
        except ValueError as e:
            print(f"✗ Error: {e}")
            sys.exit(1)
    
    else:
        print(f"Unknown command: {cmd}")
