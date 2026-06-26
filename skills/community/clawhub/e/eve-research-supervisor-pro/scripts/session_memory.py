#!/usr/bin/env python3
"""
session_memory.py — Persistent research memory across sessions
Tracks topics, papers, gaps, ideas, experiments, and decisions over weeks.
Usage:
  python3 session_memory.py save <project> <key> <value>
  python3 session_memory.py load <project>
  python3 session_memory.py summary <project>
  python3 session_memory.py list
"""

import sys
import os
import json
import datetime

BASE = os.path.expanduser("~/.openclaw/workspace/research-supervisor-pro/memory")


def get_project_file(project):
    os.makedirs(BASE, exist_ok=True)
    return os.path.join(BASE, f"{project}.json")


def load_project(project):
    path = get_project_file(project)
    if not os.path.exists(path):
        return {
            "project": project,
            "created": datetime.datetime.now().isoformat(),
            "last_updated": datetime.datetime.now().isoformat(),
            "topic": "",
            "goal": "",
            "papers": [],
            "gaps": [],
            "ideas": [],
            "experiments": [],
            "decisions": [],
            "next_steps": [],
            "sessions": []
        }
    with open(path) as f:
        return json.load(f)


def save_project(project, data):
    path = get_project_file(project)
    data["last_updated"] = datetime.datetime.now().isoformat()
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Memory saved → {path}")


def add_entry(project, key, value):
    data = load_project(project)
    timestamp = datetime.datetime.now().isoformat()

    if key in ["papers", "gaps", "ideas", "experiments", "decisions", "next_steps"]:
        entry = {"timestamp": timestamp, "content": value}
        data[key].append(entry)
    elif key in ["topic", "goal"]:
        data[key] = value
    else:
        # Generic key
        if key not in data:
            data[key] = []
        data[key].append({"timestamp": timestamp, "content": value})

    # Log session event
    data["sessions"].append({
        "timestamp": timestamp,
        "action": f"Added {key}: {str(value)[:80]}"
    })

    save_project(project, data)


def print_summary(project):
    data = load_project(project)
    print(f"\n{'='*60}")
    print(f"📚 Project: {data['project']}")
    print(f"   Topic: {data.get('topic', 'Not set')}")
    print(f"   Goal:  {data.get('goal', 'Not set')}")
    print(f"   Created: {data['created'][:10]}")
    print(f"   Last Updated: {data['last_updated'][:10]}")
    print(f"{'='*60}")
    print(f"📄 Papers tracked:      {len(data.get('papers', []))}")
    print(f"🔬 Gaps identified:     {len(data.get('gaps', []))}")
    print(f"💡 Ideas generated:     {len(data.get('ideas', []))}")
    print(f"🧪 Experiments planned: {len(data.get('experiments', []))}")
    print(f"📝 Decisions logged:    {len(data.get('decisions', []))}")
    print(f"➡️  Next steps:          {len(data.get('next_steps', []))}")

    if data.get("next_steps"):
        print(f"\n🎯 Next Steps:")
        for s in data["next_steps"][-3:]:
            print(f"  - {s['content']}")

    if data.get("sessions"):
        print(f"\n🕐 Recent Activity:")
        for s in data["sessions"][-5:]:
            print(f"  [{s['timestamp'][:16]}] {s['action']}")
    print(f"{'='*60}\n")


def list_projects():
    if not os.path.exists(BASE):
        print("No projects found.")
        return
    files = [f.replace(".json", "") for f in os.listdir(BASE) if f.endswith(".json")]
    if not files:
        print("No projects found.")
        return
    print(f"\n📂 Research Projects ({len(files)}):")
    for p in files:
        data = load_project(p)
        print(f"  - {p} | Topic: {data.get('topic','?')[:40]} | Updated: {data['last_updated'][:10]}")


def sync_from_pipeline(project, papers_dir="papers_pdf"):
    """Auto-sync papers from pipeline output into memory."""
    data = load_project(project)
    metadata_path = f"{papers_dir}/metadata.json"
    if os.path.exists(metadata_path):
        with open(metadata_path) as f:
            papers = json.load(f)
        existing_ids = {p["content"].get("arxiv_id") for p in data["papers"] if isinstance(p.get("content"), dict)}
        new = 0
        for p in papers:
            if p.get("arxiv_id") not in existing_ids:
                data["papers"].append({
                    "timestamp": datetime.datetime.now().isoformat(),
                    "content": {
                        "arxiv_id": p.get("arxiv_id"),
                        "title": p.get("title"),
                        "authors": p.get("authors", [])[:3],
                        "published": p.get("published", "")[:10]
                    }
                })
                new += 1
        save_project(project, data)
        print(f"✅ Synced {new} new papers into memory")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    action = sys.argv[1]

    if action == "list":
        list_projects()
    elif action == "load" and len(sys.argv) >= 3:
        print_summary(sys.argv[2])
    elif action == "summary" and len(sys.argv) >= 3:
        print_summary(sys.argv[2])
    elif action == "save" and len(sys.argv) >= 5:
        add_entry(sys.argv[2], sys.argv[3], sys.argv[4])
    elif action == "sync" and len(sys.argv) >= 3:
        papers_dir = sys.argv[3] if len(sys.argv) > 3 else "papers_pdf"
        sync_from_pipeline(sys.argv[2], papers_dir)
    else:
        print(__doc__)
