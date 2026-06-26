#!/usr/bin/env python3
"""
Defold Dependency Helper - Add common libraries to game.project

Usage:
    python add_dependencies.py <game.project_path> [--druid] [--defsave] [--monarch] [--all]

Examples:
    python add_dependencies.py game.project --all
    python add_dependencies.py game.project --druid --defsave
"""

import argparse
import sys
from pathlib import Path

DEPENDENCIES = {
    "druid": "https://github.com/Insality/druid/archive/refs/tags/1.2.2.zip",
    "defsave": "https://github.com/subsoap/defsave/archive/refs/tags/v1.2.6.zip",
    "monarch": "https://github.com/insality/defold-monarch/archive/1.0.zip",
    "a-star": "https://github.com/defold/a-star/archive/refs/tags/1.0.zip",
    "behavior-tree": "https://github.com/defold/def-behavior-tree/archive/refs/tags/1.0.zip"
}


def add_dependency(project_path, dep_name):
    dep_url = DEPENDENCIES.get(dep_name)
    if not dep_url:
        print(f"Unknown dependency: {dep_name}")
        return False
    
    path = Path(project_path)
    if not path.exists():
        print(f"File not found: {project_path}")
        return False
    
    content = path.read_text()
    
    if dep_url in content:
        print(f"Already exists: {dep_name}")
        return True
    
    if "dependencies =" not in content:
        content += "\n[project]\ndependencies =\n"
    
    lines = content.split("\n")
    dep_line = f"  {dep_url}"
    
    for i, line in enumerate(lines):
        if line.strip().startswith("dependencies"):
            lines.insert(i + 1, dep_line)
            break
    
    path.write_text("\n".join(lines))
    print(f"Added: {dep_name}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Add Defold dependencies")
    parser.add_argument("project", help="Path to game.project file")
    parser.add_argument("--druid", action="store_true", help="Add Druid UI framework")
    parser.add_argument("--defsave", action="store_true", help="Add DefSave")
    parser.add_argument("--monarch", action="store_true", help="Add Monarch screen manager")
    parser.add_argument("--all", action="store_true", help="Add all recommended dependencies")
    
    args = parser.parse_args()
    
    deps_to_add = []
    if args.all:
        deps_to_add = ["druid", "defsave", "monarch"]
    else:
        if args.druid: deps_to_add.append("druid")
        if args.defsave: deps_to_add.append("defsave")
        if args.monarch: deps_to_add.append("monarch")
    
    if not deps_to_add:
        print("No dependencies specified. Use --all or specific flags.")
        sys.exit(1)
    
    for dep in deps_to_add:
        add_dependency(args.project, dep)
    
    print(f"\nUpdated: {args.project}")
    print("Restart Defold Editor to load new dependencies.")


if __name__ == "__main__":
    main()