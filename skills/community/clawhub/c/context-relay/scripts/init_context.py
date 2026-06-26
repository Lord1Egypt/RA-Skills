#!/usr/bin/env python3
"""
Context Relay - Project Context Initialization Script

Creates standard context file structure in a project directory:
- PROJECT.md (Project metadata template)
- state.json (Current state)
- decisions.md (Architecture decision records)
- todos.json (Todo list)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def get_local_timezone():
    """Get local timezone offset"""
    import time
    if time.daylight:
        offset = -time.altzone // 3600
    else:
        offset = -time.timezone // 3600
    
    hours = abs(offset)
    sign = '+' if offset >= 0 else '-'
    return f"{sign}{hours:02d}:00"


def init_context(project_path: str, force: bool = False):
    """Initialize project context"""
    project_dir = Path(project_path).resolve()
    
    if not project_dir.exists():
        print(f"❌ Directory does not exist: {project_dir}")
        return False
    
    # File paths
    project_md = project_dir / "PROJECT.md"
    state_json = project_dir / "state.json"
    decisions_md = project_dir / "decisions.md"
    todos_json = project_dir / "todos.json"
    
    # Check for existing files
    existing_files = []
    for f in [project_md, state_json, decisions_md, todos_json]:
        if f.exists():
            existing_files.append(f.name)
    
    if existing_files and not force:
        print(f"⚠️  The following files already exist: {', '.join(existing_files)}")
        print("    Use --force option to overwrite existing files")
        return False
    
    # Timezone
    tz = get_local_timezone()
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + tz
    
    # Create PROJECT.md
    project_content = """# Project Name

## One-Line Description
[What this project is, what problem it solves]

## Tech Stack
- Frontend:
- Backend:
- Database:
- Deployment:

## Directory Structure
/src        - Source code
/docs       - Documentation
/tests      - Tests

## Key Constraints
[Rules that must be followed, such as API compatibility, performance requirements]

## Related Documents
- Architecture decisions: decisions.md
- Current state: state.json
- Todo items: todos.json
"""
    
    # Create state.json
    state_content = {
        "version": "1.0",
        "phase": "planning",
        "current_task": "",
        "progress": {
            "completed": [],
            "in_progress": None,
            "blocked": [],
            "next_steps": []
        },
        "metrics": {
            "total_tasks": 0,
            "completed_tasks": 0,
            "blocked_tasks": 0
        },
        "last_update": now,
        "last_session": None,
        "notes": ""
    }
    
    # Create decisions.md
    decisions_content = """# Architecture Decision Records

This document records important architecture decisions in the project using the ADR (Architecture Decision Record) format.

## ADR Template

### ADR-XXX: [Decision Title]

### Metadata
- **Date**: YYYY-MM-DD
- **Status**: Accepted / Deprecated / Superseded
- **Decider**: [Name or Team]

### Context
[Why is this decision needed? What is the problem?]

### Decision
[What decision was made? What are the specifics?]

### Rationale
[Why was this option chosen? What alternatives were considered?]

### Consequences
[What are the implications of this decision? Positive and negative?]

---

## ADR-001: [First Decision]
...
"""
    
    # Create todos.json
    todos_content = {
        "todos": [],
        "completed": [],
        "metadata": {
            "last_review": now,
            "total_created": 0,
            "total_completed": 0
        }
    }
    
    # Write files
    try:
        project_md.write_text(project_content, encoding='utf-8')
        state_json.write_text(json.dumps(state_content, indent=2, ensure_ascii=False), encoding='utf-8')
        decisions_md.write_text(decisions_content, encoding='utf-8')
        todos_json.write_text(json.dumps(todos_content, indent=2, ensure_ascii=False), encoding='utf-8')
        
        print(f"✅ Context files created in {project_dir}:")
        print(f"   ├── PROJECT.md    (Project metadata)")
        print(f"   ├── state.json    (Current state)")
        print(f"   ├── decisions.md  (Architecture decisions)")
        print(f"   └── todos.json    (Todo list)")
        print()
        print("📝 Next step: Edit PROJECT.md to fill in project information")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create files: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Initialize project context file structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python init_context.py /path/to/project
  python init_context.py .                    # Current directory
  python init_context.py ./my-project --force # Overwrite existing files
        """
    )
    
    parser.add_argument(
        "path",
        help="Project directory path"
    )
    
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Overwrite existing files"
    )
    
    args = parser.parse_args()
    
    success = init_context(args.path, args.force)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()