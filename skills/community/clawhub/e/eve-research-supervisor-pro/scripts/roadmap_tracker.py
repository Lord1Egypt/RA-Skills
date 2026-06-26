#!/usr/bin/env python3
"""
roadmap_tracker.py — Track research roadmap progress (resumable across sessions)
Usage:
  python3 roadmap_tracker.py init   <project> <idea_title> <gpu> <time_weeks>
  python3 roadmap_tracker.py status <project>
  python3 roadmap_tracker.py done   <project> <step_id>       (e.g. A1, B3)
  python3 roadmap_tracker.py block  <project> <step_id> <reason>
  python3 roadmap_tracker.py unblock <project> <step_id>
  python3 roadmap_tracker.py next   <project>
  python3 roadmap_tracker.py list   <project>
"""

import sys
import os
import json
import datetime

BASE = os.path.expanduser("~/.openclaw/workspace/research-supervisor-pro/research")


def get_progress_file(project):
    path = os.path.join(BASE, project)
    os.makedirs(path, exist_ok=True)
    return os.path.join(path, "roadmap_progress.json")


def load_progress(project):
    path = get_progress_file(project)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def save_progress(project, data):
    path = get_progress_file(project)
    data["last_updated"] = datetime.date.today().isoformat()
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def build_roadmap(idea_title, gpu, time_weeks):
    """Generate roadmap steps based on user setup."""
    phases = [
        {
            "id": "A",
            "name": "Environment Setup",
            "days": max(1, time_weeks // 6),
            "steps": [
                {"id": "A1", "name": "Install Python dependencies (torch, diffusers, etc.)", "status": "pending"},
                {"id": "A2", "name": f"Verify {gpu} GPU/compute is working", "status": "pending"},
                {"id": "A3", "name": "Download base models (SD, HiDDeN, etc.)", "status": "pending"},
            ]
        },
        {
            "id": "B",
            "name": "Baseline Implementation",
            "days": max(3, time_weeks // 4),
            "steps": [
                {"id": "B1", "name": "Clone/implement Baseline 1", "status": "pending"},
                {"id": "B2", "name": "Clone/implement Baseline 2", "status": "pending"},
                {"id": "B3", "name": "Run baseline experiments", "status": "pending"},
                {"id": "B4", "name": "Record baseline numbers (BER, Bit Acc, PSNR, SSIM)", "status": "pending"},
            ]
        },
        {
            "id": "C",
            "name": "Proposed Method",
            "days": max(5, time_weeks // 3),
            "steps": [
                {"id": "C1", "name": "Implement proposed approach", "status": "pending"},
                {"id": "C2", "name": "Train on dataset", "status": "pending"},
                {"id": "C3", "name": "Evaluate on metrics", "status": "pending"},
                {"id": "C4", "name": "Run ablation study", "status": "pending"},
            ]
        },
        {
            "id": "D",
            "name": "Analysis",
            "days": max(2, time_weeks // 5),
            "steps": [
                {"id": "D1", "name": "Compare results against all baselines", "status": "pending"},
                {"id": "D2", "name": "Generate figures and tables (EVE auto-generates)", "status": "pending"},
                {"id": "D3", "name": "Statistical significance / robustness tests", "status": "pending"},
            ]
        },
        {
            "id": "E",
            "name": "Paper Writing",
            "days": max(3, time_weeks // 4),
            "steps": [
                {"id": "E1", "name": "Fill experiment_data_template.json with real results", "status": "pending"},
                {"id": "E2", "name": "EVE generates all figures + LaTeX tables", "status": "pending"},
                {"id": "E3", "name": "EVE writes full LaTeX research paper", "status": "pending"},
                {"id": "E4", "name": "Review, revise, and submit", "status": "pending"},
            ]
        }
    ]
    return phases


def init_roadmap(project, idea_title, gpu, time_weeks):
    phases = build_roadmap(idea_title, gpu, int(time_weeks))
    all_steps = [s["id"] for p in phases for s in p["steps"]]

    data = {
        "project": project,
        "idea_title": idea_title,
        "gpu": gpu,
        "time_weeks": time_weeks,
        "created": datetime.date.today().isoformat(),
        "last_updated": datetime.date.today().isoformat(),
        "current_phase": "A",
        "current_step": "A1",
        "completed": [],
        "blocked": [],
        "all_steps": all_steps,
        "phases": phases
    }

    save_progress(project, data)

    # Also write human-readable roadmap.md
    roadmap_path = os.path.join(BASE, project, "roadmap.md")
    total_days = sum(p["days"] for p in phases)
    with open(roadmap_path, "w") as f:
        f.write(f"# 🗺️ Research Roadmap — {idea_title}\n\n")
        f.write(f"**GPU:** {gpu} | **Timeline:** {time_weeks} weeks (~{total_days} days)\n\n")
        f.write("```\n")
        for phase in phases:
            f.write(f"\nPHASE {phase['id']} — {phase['name']}  [~{phase['days']} days]\n")
            for step in phase["steps"]:
                f.write(f"  ├── {step['id']}. {step['name']}\n")
        f.write("```\n\n")
        f.write("## Progress\n\n")
        f.write("Track via: `python3 roadmap_tracker.py status <project>`\n")

    print(f"✅ Roadmap initialized for: {idea_title}")
    print(f"   Steps: {len(all_steps)} across {len(phases)} phases")
    print(f"   Saved: roadmap_progress.json + roadmap.md")
    return data


def print_status(project):
    data = load_progress(project)
    if not data:
        print(f"❌ No roadmap found for project: {project}")
        print(f"   Run: python3 roadmap_tracker.py init <project> <title> <gpu> <weeks>")
        return

    completed = set(data.get("completed", []))
    blocked   = {b["step"]: b["reason"] for b in data.get("blocked", [])}
    all_steps = data.get("all_steps", [])
    total     = len(all_steps)
    done      = len(completed)
    pct       = int(done / total * 100) if total else 0
    bar       = "█" * (pct // 5) + "░" * (20 - pct // 5)

    print(f"\n{'━'*56}")
    print(f" 🗺️  RESEARCH ROADMAP — {data['idea_title']}")
    print(f" Project: {project} | GPU: {data['gpu']} | {data['time_weeks']} weeks")
    print(f" Progress: [{bar}] {pct}% ({done}/{total} steps)")
    print(f"{'━'*56}")

    for phase in data["phases"]:
        phase_done = all(s["id"] in completed for s in phase["steps"])
        icon = "✅" if phase_done else "⏳"
        print(f"\n {icon} PHASE {phase['id']} — {phase['name']}")
        for step in phase["steps"]:
            sid = step["id"]
            if sid in completed:
                mark = "✅"
            elif sid in blocked:
                mark = f"🚫 BLOCKED: {blocked[sid][:40]}"
            elif sid == data.get("current_step"):
                mark = "▶️  ← CURRENT"
            else:
                mark = "⬜"
            print(f"    {mark}  {sid}. {step['name']}")

    print(f"\n{'━'*56}")
    print(f" 📍 Current step: {data.get('current_step','?')}")
    print(f" ⏳ Remaining:    {total - done} steps")
    print(f"{'━'*56}\n")


def mark_done(project, step_id):
    data = load_progress(project)
    if not data:
        print(f"❌ No roadmap found for: {project}")
        return

    step_id = step_id.upper()
    if step_id not in data["completed"]:
        data["completed"].append(step_id)

    # Remove from blocked if was blocked
    data["blocked"] = [b for b in data["blocked"] if b["step"] != step_id]

    # Find next pending step
    all_steps = data["all_steps"]
    remaining = [s for s in all_steps if s not in data["completed"]]
    data["current_step"] = remaining[0] if remaining else "COMPLETE"

    # Update current phase
    if remaining:
        data["current_phase"] = remaining[0][0]

    save_progress(project, data)
    print(f"✅ Step {step_id} marked complete!")
    if remaining:
        print(f"   Next step: {remaining[0]}")
    else:
        print(f"   🎉 ALL STEPS COMPLETE! Ready to write your paper.")


def mark_blocked(project, step_id, reason):
    data = load_progress(project)
    if not data:
        print(f"❌ No roadmap found: {project}")
        return
    step_id = step_id.upper()
    data["blocked"] = [b for b in data["blocked"] if b["step"] != step_id]
    data["blocked"].append({"step": step_id, "reason": reason, "since": datetime.date.today().isoformat()})
    save_progress(project, data)
    print(f"🚫 Step {step_id} marked as blocked: {reason}")


def unblock(project, step_id):
    data = load_progress(project)
    if not data:
        return
    step_id = step_id.upper()
    data["blocked"] = [b for b in data["blocked"] if b["step"] != step_id]
    save_progress(project, data)
    print(f"✅ Step {step_id} unblocked!")


def next_step(project):
    data = load_progress(project)
    if not data:
        print(f"❌ No roadmap found: {project}")
        return
    step_id = data.get("current_step", "")
    if step_id == "COMPLETE":
        print("🎉 All steps complete! Ready to write your paper.")
        return
    # Find step details
    for phase in data["phases"]:
        for step in phase["steps"]:
            if step["id"] == step_id:
                print(f"\n📍 Next Step: {step_id} — {step['name']}")
                print(f"   Phase: {phase['id']} — {phase['name']}")
                return


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    action = sys.argv[1]

    if action == "init" and len(sys.argv) >= 6:
        init_roadmap(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif action == "status" and len(sys.argv) >= 3:
        print_status(sys.argv[2])
    elif action == "done" and len(sys.argv) >= 4:
        mark_done(sys.argv[2], sys.argv[3])
    elif action == "block" and len(sys.argv) >= 5:
        mark_blocked(sys.argv[2], sys.argv[3], sys.argv[4])
    elif action == "unblock" and len(sys.argv) >= 4:
        unblock(sys.argv[2], sys.argv[3])
    elif action == "next" and len(sys.argv) >= 3:
        next_step(sys.argv[2])
    else:
        print(__doc__)
