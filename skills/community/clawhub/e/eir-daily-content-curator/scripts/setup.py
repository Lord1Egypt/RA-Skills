#!/usr/bin/env python3
"""
Eir Daily Content Curator — Setup

Creates workspace directories, writes config/settings.json, copies default sources.
Designed to be called by an OpenClaw agent with pre-collected settings.

Usage:
  # Agent-driven (non-interactive) — pass all settings as JSON:
  python3 scripts/setup.py --init --settings '{"mode":"standalone","language":"zh",...}'

  # Set workspace directory in skill config (run once after install):
  python3 scripts/setup.py --set-workspace /path/to/workspace

  # Check current setup:
  python3 scripts/setup.py --check

  # Show resolved workspace:
  python3 scripts/setup.py --show-workspace
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

# Skill root directory
SKILL_DIR = Path(__file__).resolve().parent.parent

# Add scripts to path for pipeline imports
sys.path.insert(0, str(SKILL_DIR / "scripts"))
from pipeline.workspace import resolve_workspace


def set_workspace(workspace_dir: str) -> Path:
    """Write workspace_dir into skill's config/settings.json so all scripts can find it."""
    workspace = Path(workspace_dir).expanduser().resolve()
    
    # Ensure workspace exists
    (workspace / "config").mkdir(parents=True, exist_ok=True)
    (workspace / "data").mkdir(parents=True, exist_ok=True)
    (workspace / "data" / "snippets").mkdir(parents=True, exist_ok=True)
    (workspace / "data" / "generated").mkdir(parents=True, exist_ok=True)
    
    # Write workspace_dir into skill's config/settings.json
    skill_settings_file = SKILL_DIR / "config" / "settings.json"
    skill_settings = {}
    if skill_settings_file.exists():
        try:
            skill_settings = json.loads(skill_settings_file.read_text())
        except (json.JSONDecodeError, KeyError):
            pass
    
    skill_settings["workspace_dir"] = str(workspace)
    skill_settings_file.write_text(json.dumps(skill_settings, indent=2, ensure_ascii=False))
    
    print(json.dumps({"ok": True, "workspace": str(workspace)}))
    return workspace


def init_workspace(settings: dict) -> dict:
    """Initialize workspace with the given settings.
    
    Creates config/settings.json and copies default sources if needed.
    Returns a status dict.
    """
    workspace = resolve_workspace()
    config_dir = workspace / "config"
    data_dir = workspace / "data"
    
    # Ensure directories
    config_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "snippets").mkdir(exist_ok=True)
    (data_dir / "generated").mkdir(exist_ok=True)
    
    # Write settings.json into workspace
    settings_file = config_dir / "settings.json"
    settings_file.write_text(json.dumps(settings, indent=2, ensure_ascii=False))
    
    # Copy default sources.json if not present
    sources_file = config_dir / "sources.json"
    if not sources_file.exists():
        skill_sources = SKILL_DIR / "config" / "sources.json"
        if skill_sources.exists():
            shutil.copy(skill_sources, sources_file)
    
    result = {
        "ok": True,
        "workspace": str(workspace),
        "settings_file": str(settings_file),
        "sources_file": str(sources_file),
        "mode": settings.get("mode", "standalone"),
    }
    print(json.dumps(result))
    return result


def check_setup() -> dict:
    """Check current setup status. Returns JSON."""
    workspace = resolve_workspace()
    settings_file = workspace / "config" / "settings.json"
    sources_file = workspace / "config" / "sources.json"
    eir_json = workspace / "config" / "eir.json"
    
    result = {
        "workspace": str(workspace),
        "workspace_exists": workspace.exists(),
        "settings_exists": settings_file.exists(),
        "sources_exists": sources_file.exists(),
        "eir_connected": eir_json.exists(),
        "mode": None,
        "language": None,
        "data_dir_exists": (workspace / "data").exists(),
    }
    
    if settings_file.exists():
        try:
            settings = json.loads(settings_file.read_text())
            result["mode"] = settings.get("mode")
            result["language"] = settings.get("language")
            result["search_providers"] = settings.get("search", {}).get("providers", [])
        except (json.JSONDecodeError, KeyError):
            pass
    
    print(json.dumps(result, indent=2))
    return result


def main():
    parser = argparse.ArgumentParser(description="Eir Content Curator — Setup")
    parser.add_argument("--check", action="store_true", help="Check current setup status (JSON output)")
    parser.add_argument("--show-workspace", action="store_true", help="Print resolved workspace path")
    parser.add_argument("--set-workspace", metavar="PATH", help="Set workspace directory")
    parser.add_argument("--init", action="store_true", help="Initialize workspace with --settings JSON")
    parser.add_argument("--settings", metavar="JSON", help="Settings JSON string (use with --init)")
    parser.add_argument("--settings-file", metavar="PATH", help="Path to settings JSON file (alternative to --settings)")
    args = parser.parse_args()

    if args.show_workspace:
        print(str(resolve_workspace()))
        return

    if args.set_workspace:
        set_workspace(args.set_workspace)
        return

    if args.check:
        check_setup()
        return

    if args.init:
        if args.settings_file:
            try:
                settings = json.loads(Path(args.settings_file).read_text())
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(json.dumps({"ok": False, "error": f"Failed to read settings file: {e}"}))
                sys.exit(1)
        elif args.settings:
            try:
                settings = json.loads(args.settings)
            except json.JSONDecodeError as e:
                print(json.dumps({"ok": False, "error": f"Invalid JSON: {e}"}))
                sys.exit(1)
        else:
            print(json.dumps({"ok": False, "error": "--init requires --settings or --settings-file"}))
            sys.exit(1)
        init_workspace(settings)
        return

    # No args — show help
    parser.print_help()


if __name__ == "__main__":
    main()
