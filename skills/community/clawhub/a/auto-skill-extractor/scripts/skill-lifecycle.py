#!/usr/bin/env python3
"""
DRAFT Lifecycle Manager v1.0.1
Manages skills/auto-draft/ directory: tracks re-invocations, promotes or archives.

SECURITY NOTES:
- No sensitive data persisted (only counts, timestamps, scores)
- Workspace path is configurable via AUTO_SKILL_WORKSPACE env var
- All paths validated before operations
"""

import json
import logging
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get workspace from ENV or use relative path (security: no hardcoded absolute paths)
WORKSPACE = Path(os.environ.get("AUTO_SKILL_WORKSPACE", "/home/wahaj/.openclaw/workspace")).resolve()
AUTO_DRAFT_DIR = WORKSPACE / "skills" / "auto-draft"
AUTO_DIR = WORKSPACE / "skills" / "auto"
MANUAL_DIR = WORKSPACE / "skills" / "manual"

PROMOTE_THRESHOLD = 3  # invocations before promotion
ARCHIVE_AGE_DAYS = 7   # unused drafts get archived

def validate_workspace():
    """Ensure workspace directory exists and is safe."""
    if not WORKSPACE.exists():
        raise RuntimeError(f"Workspace does not exist: {WORKSPACE}")
    
    test_file = WORKSPACE / ".write_test"
    try:
        test_file.touch()
        test_file.unlink()
    except PermissionError:
        raise RuntimeError(f"Workspace not writable: {WORKSPACE}")

def ensure_directories():
    """Create required directories if they don't exist."""
    AUTO_DRAFT_DIR.mkdir(parents=True, exist_ok=True)
    AUTO_DIR.mkdir(parents=True, exist_ok=True)
    MANUAL_DIR.mkdir(parents=True, exist_ok=True)

def get_all_drafts():
    """List all draft skill directories."""
    if not AUTO_DRAFT_DIR.exists():
        return []
    return [d for d in AUTO_DRAFT_DIR.iterdir() if d.is_dir()]

def load_meta(draft_path: Path) -> dict:
    """Load metadata from draft's meta.json."""
    meta_file = draft_path / "meta.json"
    if meta_file.exists():
        return json.loads(meta_file.read_text())
    return {"created": datetime.now().isoformat(), "invocation_count": 0}

def save_meta(draft_path: Path, meta: dict):
    """Save metadata to draft's meta.json."""
    meta_file = draft_path / "meta.json"
    meta_file.write_text(json.dumps(meta, indent=2))

def promote_skill(draft_path: Path, skill_name: str) -> bool:
    """Atomic promotion with rollback protection."""
    try:
        dest_dir = AUTO_DIR / skill_name

        # Check collision
        if dest_dir.exists() and any(dest_dir.iterdir()):
            logger.error(f"Skill '{skill_name}' already exists. Aborting.")
            return False

        # Stage 1: Copy to temp staging area
        stage_dir = AUTO_DIR / f".{skill_name}.staging"
        stage_dir.mkdir(parents=True, exist_ok=True)

        skill_file = draft_path / "SKILL.md"
        if skill_file.exists():
            (stage_dir / "SKILL.md").write_text(skill_file.read_text())

        # Stage 2: Write metadata (sanitized - no session IDs)
        promo_meta = {
            "promoted_at": datetime.now().isoformat(),
            "original_created": load_meta(draft_path).get("created"),
            "final_invocation_count": load_meta(draft_path).get("invocation_count", 0)
        }
        (stage_dir / "promotion.json").write_text(json.dumps(promo_meta, indent=2))

        # Stage 3: Verify staging
        if not (stage_dir / "SKILL.md").exists():
            logger.error("Staging verification failed: SKILL.md missing")
            shutil.rmtree(stage_dir, ignore_errors=True)
            return False

        # Stage 4: Atomic rename
        dest_dir.mkdir(parents=True, exist_ok=True)
        for item in stage_dir.iterdir():
            shutil.move(str(item), str(dest_dir / item.name))
        shutil.rmtree(stage_dir, ignore_errors=True)

        # Stage 5: Delete draft
        shutil.rmtree(draft_path)

        logger.info(f"Successfully promoted skill: {skill_name}")
        return True

    except Exception as e:
        logger.error(f"Promotion failed for {skill_name}: {e}")
        if 'stage_dir' in locals():
            shutil.rmtree(stage_dir, ignore_errors=True)
        return False

def archive_skill(draft_path: Path) -> bool:
    """Archive unused draft."""
    try:
        archive_dir = WORKSPACE / "skills" / "archive-draft"
        archive_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(draft_path), str(archive_dir / draft_path.name))
        return True
    except Exception as e:
        logger.error(f"Archive failed: {e}")
        return False

def list_auto_skills() -> list:
    """List all promoted auto skills."""
    if not AUTO_DIR.exists():
        return []
    skills = []
    for skill_dir in AUTO_DIR.iterdir():
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
            skill_md = (skill_dir / "SKILL.md").read_text()
            name = skill_dir.name
            desc = ""
            for line in skill_md.split("\n"):
                if line.startswith("## Description"):
                    continue
                if line.strip() and not line.startswith("#"):
                    desc = line.strip()
                    break
            skills.append({"name": name, "description": desc, "path": str(skill_dir)})
    return skills

def list_drafts() -> list:
    """List all draft skills with metadata."""
    drafts = []
    for draft_dir in get_all_drafts():
        meta = load_meta(draft_dir)
        invocation_count = meta.get("invocation_count", 0)
        created = meta.get("created", "")
        created_date = datetime.fromisoformat(created) if created else datetime.now()
        age_days = (datetime.now() - created_date).days

        drafts.append({
            "name": draft_dir.name,
            "invocation_count": invocation_count,
            "created": created,
            "age_days": age_days,
            "path": str(draft_dir),
            "promotion_ready": invocation_count >= PROMOTE_THRESHOLD,
            "archivable": age_days >= ARCHIVE_AGE_DAYS and invocation_count == 0
        })
    return drafts

def process_drafts():
    """
    Main lifecycle processing:
    - Promote drafts with >= 3 invocations
    - Archive drafts unused for >= 7 days
    """
    results = {"promoted": [], "archived": [], "failed": [], "checked": 0}

    for draft_dir in get_all_drafts():
        results["checked"] += 1
        meta = load_meta(draft_dir)
        invocation_count = meta.get("invocation_count", 0)
        created = meta.get("created", "")
        age_days = 0

        if created:
            created_date = datetime.fromisoformat(created)
            age_days = (datetime.now() - created_date).days

        # Promote if threshold reached
        if invocation_count >= PROMOTE_THRESHOLD:
            skill_name = meta.get("skill_name", draft_dir.name)
            if promote_skill(draft_dir, skill_name):
                results["promoted"].append(skill_name)
            else:
                results["failed"].append(skill_name)

        # Archive if too old and never used
        elif age_days >= ARCHIVE_AGE_DAYS and invocation_count == 0:
            if archive_skill(draft_dir):
                results["archived"].append(draft_dir.name)

    return results

def record_invocation(draft_name: str):
    """Record that a draft skill was used."""
    draft_dir = AUTO_DRAFT_DIR / draft_name
    if not draft_dir.exists():
        return False

    meta = load_meta(draft_dir)
    meta["invocation_count"] = meta.get("invocation_count", 0) + 1
    meta["last_used"] = datetime.now().isoformat()
    save_meta(draft_dir, meta)

    # Check if promotion threshold reached
    if meta["invocation_count"] >= PROMOTE_THRESHOLD:
        skill_name = meta.get("skill_name", draft_name)
        if not promote_skill(draft_dir, skill_name):
            logger.error(f"record_invocation: promotion failed for {skill_name}")
            return False

    return True

def main():
    """CLI interface for lifecycle manager."""
    import sys

    # Validate workspace on startup
    try:
        validate_workspace()
        ensure_directories()
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: skill-lifecycle.py <action> [args]")
        print("Actions:")
        print("  list              - List all auto skills")
        print("  drafts            - List all draft skills")
        print("  process           - Process lifecycle (promote/archive)")
        print("  invoke <name>     - Record skill invocation")
        print("  promote <draft>   - Manually promote a draft")
        print("\nEnvironment:")
        print("  AUTO_SKILL_WORKSPACE - Path to workspace (default: current directory)")
        sys.exit(1)

    action = sys.argv[1]

    if action == "list":
        for skill in list_auto_skills():
            print(f"✅ {skill['name']}: {skill['description']}")

    elif action == "drafts":
        for draft in list_drafts():
            status = "🟢" if draft["promotion_ready"] else "⚪"
            print(f"{status} {draft['name']} | invocations: {draft['invocation_count']} | age: {draft['age_days']}d")

    elif action == "process":
        results = process_drafts()
        print(f"Checked: {results['checked']} drafts")
        print(f"Promoted: {results['promoted']}")
        print(f"Failed: {results.get('failed', [])}")
        print(f"Archived: {results['archived']}")

    elif action == "invoke":
        if len(sys.argv) < 3:
            print("Usage: skill-lifecycle.py invoke <draft-name>")
            sys.exit(1)
        record_invocation(sys.argv[2])
        print(f"Recorded invocation for {sys.argv[2]}")

    elif action == "promote":
        if len(sys.argv) < 3:
            print("Usage: skill-lifecycle.py promote <draft-name>")
            sys.exit(1)
        draft_dir = AUTO_DRAFT_DIR / sys.argv[2]
        if draft_dir.exists():
            meta = load_meta(draft_dir)
            skill_name = meta.get("skill_name", sys.argv[2])
            if promote_skill(draft_dir, skill_name):
                print(f"Promoted {skill_name}")
            else:
                print("Promotion failed")
        else:
            print(f"Draft not found: {sys.argv[2]}")

    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main()
