#!/usr/bin/env python3
"""
List all installed skills with their names and descriptions.
"""
import os
import json
import yaml
from pathlib import Path

def list_skills(skills_root=None):
    if skills_root is None:
        # Try multiple locations
        possible_roots = [
            Path("/var/root/.openclaw/skills"),
            Path("/var/root/.openclaw/workspace/skills"),
            Path("/usr/local/lib/node_modules/openclaw/skills"),
        ]
        for root in possible_roots:
            if root.exists():
                skills_root = root
                break
        if skills_root is None:
            print("No skills directory found")
            return

    skills = []
    for skill_dir in sorted(skills_root.iterdir()):
        if skill_dir.is_dir():
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                try:
                    content = skill_file.read_text(encoding="utf-8")
                    # Parse YAML frontmatter
                    if content.startswith("---"):
                        end = content.find("---", 3)
                        if end != -1:
                            frontmatter = yaml.safe_load(content[3:end])
                            name = frontmatter.get("name", skill_dir.name)
                            desc = frontmatter.get("description", "No description")
                            skills.append({
                                "name": name,
                                "description": desc,
                                "path": str(skill_dir)
                            })
                except Exception as e:
                    skills.append({
                        "name": skill_dir.name,
                        "description": f"Error reading: {e}",
                        "path": str(skill_dir)
                    })

    # Output as formatted list
    print(f"# Skills in {skills_root}\n")
    for s in skills:
        print(f"## {s['name']}")
        print(f"{s['description']}")
        print()

if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else None
    list_skills(Path(root) if root else None)
