#!/usr/bin/env python3
"""
project_init.py — Initialize a new research project folder (Semi-Manual mode)
Creates: plan.md, notes.md, report.md, memory.md
Usage: python3 project_init.py "<project_title>" [base_dir]
"""

import sys
import os
import re
import datetime
import json

BASE = os.path.expanduser("~/.openclaw/workspace/research-supervisor-pro/research")


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text[:50]


def init_project(title, base_dir=BASE):
    slug = slugify(title)
    project_dir = os.path.join(base_dir, slug)

    if os.path.exists(project_dir):
        print(f"⚠️  Project already exists: {project_dir}")
        print(f"   Loading existing project...")
        return project_dir, slug

    os.makedirs(project_dir, exist_ok=True)
    os.makedirs(os.path.join(project_dir, "papers_pdf"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "figures"), exist_ok=True)

    date = datetime.date.today().isoformat()

    # plan.md
    with open(os.path.join(project_dir, "plan.md"), "w") as f:
        f.write(f"# Research Plan — {title}\n\n")
        f.write(f"**Created:** {date}\n\n")
        f.write("## Goal\n[Define your research goal here]\n\n")
        f.write("## Research Questions\n1. \n2. \n3. \n\n")
        f.write("## Methodology\n[Outline your approach]\n\n")
        f.write("## Timeline\n| Milestone | Target Date | Status |\n|---|---|---|\n| Literature Review | | ⬜ |\n| Gap Analysis | | ⬜ |\n| Experiment Design | | ⬜ |\n| Implementation | | ⬜ |\n| Paper Writing | | ⬜ |\n\n")
        f.write("## Target Venue\n[Conference / Journal]\n")

    # notes.md
    with open(os.path.join(project_dir, "notes.md"), "w") as f:
        f.write(f"# Research Notes — {title}\n\n")
        f.write(f"**Created:** {date}\n\n")
        f.write("## Key Papers\n[Papers will be added here by pdf_parser.py]\n\n")
        f.write("## Key Insights\n\n## Questions to Answer\n")

    # report.md
    with open(os.path.join(project_dir, "report.md"), "w") as f:
        f.write(f"# Research Report — {title}\n\n")
        f.write(f"**Created:** {date}\n\n")
        f.write("## Abstract\n[To be written]\n\n")
        f.write("## Progress\n- [ ] Literature review complete\n- [ ] Gaps identified\n- [ ] Ideas generated\n- [ ] Experiments planned\n- [ ] Paper drafted\n")

    # memory.md
    with open(os.path.join(project_dir, "memory.md"), "w") as f:
        f.write(f"# Project Memory — {title}\n\n")
        f.write(f"**Created:** {date}\n\n")
        f.write("## Decisions Made\n\n## Key Findings\n\n## Next Steps\n\n## Session Log\n")

    # meta.json
    meta = {
        "title": title,
        "slug": slug,
        "created": date,
        "status": "active",
        "mode": "semi-manual"
    }
    with open(os.path.join(project_dir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    print(f"✅ Project initialized: {project_dir}")
    print(f"   Files created: plan.md, notes.md, report.md, memory.md, meta.json")
    print(f"   Folders: papers_pdf/, figures/")
    return project_dir, slug


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python3 project_init.py "<project_title>" [base_dir]')
        sys.exit(1)
    title    = sys.argv[1]
    base_dir = sys.argv[2] if len(sys.argv) > 2 else BASE
    init_project(title, base_dir)
