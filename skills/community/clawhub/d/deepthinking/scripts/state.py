#!/usr/bin/env python3
"""
DeepThinking State Manager
==========================
Persists session state to ~/.deepthinking/current/state.json
The OpenClaw agent calls this script to read/write state between turns.
"""
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

STATE_DIR = Path.home() / ".deepthinking" / "current"
STATE_FILE = STATE_DIR / "state.json"
ARCHIVE_DIR = Path.home() / ".deepthinking" / "archive"

MODULES = {
    "diverge": {
        "name": "Diverge",
        "purpose": "Generate possibilities without judgment",
        "use_when": "Stuck on one path",
        "prompts": [
            "Give me the first thing that comes to mind. Don't filter.",
            "Now the opposite. What would surprise everyone?",
            "Past the obvious ones. What would you never say out loud?",
            "If money didn't matter? If you had zero money?",
            "What would your 80-year-old self wish you tried?"
        ],
        "exchanges": [3, 7]
    },
    "converge": {
        "name": "Converge",
        "purpose": "Filter with criteria. Kill options ruthlessly.",
        "use_when": "Too many options",
        "prompts": [
            "What 3 things ACTUALLY matter here? Not should-matter.",
            "Which options fail on criterion #1?",
            "Which survive all three?",
            "You're hesitating on one you should cut. Why?"
        ],
        "exchanges": [3, 5]
    },
    "invert": {
        "name": "Invert",
        "purpose": "Stress-test. Pre-mortem. Steelman the opposite.",
        "use_when": "Too attached to one idea",
        "prompts": [
            "I'm going to argue against your idea. If it survives, you'll trust it more.",
            "It's 12 months from now and this failed. What happened?",
            "Strongest argument against this. How do you respond?",
            "What are you deliberately not thinking about?"
        ],
        "exchanges": [3, 5]
    },
    "prototype": {
        "name": "Prototype",
        "purpose": "Make it concrete. 48 hours, $0.",
        "use_when": "Stuck in abstraction",
        "prompts": [
            "Smallest version testable in 48h spending nothing?",
            "ONE thing you'd measure to know if it worked?",
            "What can you do TODAY?",
            "Who's the first person you'd show this to?"
        ],
        "exchanges": [3, 5]
    },
    "mirror": {
        "name": "Mirror",
        "purpose": "Reflect patterns the user can't see.",
        "use_when": "Orbiting same theme",
        "prompts": [
            "You keep coming back to the same theme. Do you see it?",
            "Your energy shifts when you talk about this. What's that?",
            "What you say you want and what you describe are different."
        ],
        "exchanges": [2, 4]
    },
    "reframe": {
        "name": "Reframe",
        "purpose": "Change the problem entirely.",
        "use_when": "Solving the wrong problem",
        "prompts": [
            "You might be solving the wrong problem.",
            "What if the question isn't about that at all?",
            "You're assuming something that might not be true."
        ],
        "exchanges": [2, 4]
    },
    "commit": {
        "name": "Commit",
        "purpose": "Force decision. First action. Deadline.",
        "use_when": "Has clarity but won't act",
        "prompts": [
            "You already know. Say it.",
            "First ACTION. Not plan. First thing you'll do.",
            "By when? A day, not 'soon.'",
            "Who will you tell? Commitment needs a witness."
        ],
        "exchanges": [3, 5]
    }
}


def default_state(topic):
    return {
        "version": "0.1.0",
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
        "topic": topic,
        "phase": "excavation",
        "excavation_layer": 0,
        "profile": {
            "surface_ask": topic,
            "life_context": "",
            "energy_map": "",
            "fear": "",
            "real_want": "",
            "alignment": ""
        },
        "pipeline": {
            "name": "",
            "modules": [],
            "current_index": 0
        },
        "module_outputs": {},
        "exchange_count": 0
    }


def load():
    if not STATE_FILE.exists():
        return None
    with open(STATE_FILE) as f:
        return json.load(f)


def save(state):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state["updated"] = datetime.now().isoformat()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def cmd_init(args):
    topic = args[0] if args else "untitled"
    state = default_state(topic)
    save(state)
    print(json.dumps({"status": "initialized", "topic": topic, "phase": "excavation"}))


def cmd_status(args):
    state = load()
    if not state:
        print(json.dumps({"status": "no_session"}))
        return
    out = {
        "topic": state["topic"],
        "phase": state["phase"],
        "excavation_layer": state["excavation_layer"],
        "pipeline": state["pipeline"]["name"] or "(not set)",
        "current_module": _current_module_name(state),
        "created": state["created"],
        "updated": state["updated"]
    }
    print(json.dumps(out))


def cmd_get(args):
    state = load()
    if not state:
        print(json.dumps({"error": "no session"}))
        return
    key = args[0] if args else ""
    if key == "profile":
        print(json.dumps(state["profile"], ensure_ascii=False))
    elif key == "outputs":
        print(json.dumps(state["module_outputs"], ensure_ascii=False))
    elif key == "excavation_layer":
        print(json.dumps({"layer": state["excavation_layer"]}))
    elif key == "phase":
        print(json.dumps({"phase": state["phase"]}))
    else:
        print(json.dumps({"error": f"unknown key: {key}"}))


def cmd_save_layer(args):
    state = load()
    if not state:
        print(json.dumps({"error": "no session"}))
        return
    layer = int(args[0])
    summary = " ".join(args[1:])
    fields = ["surface_ask", "life_context", "energy_map", "fear", "real_want"]
    if 0 <= layer < len(fields):
        state["profile"][fields[layer]] = summary
        save(state)
        print(json.dumps({"saved": fields[layer], "layer": layer}))
    else:
        print(json.dumps({"error": f"invalid layer: {layer}"}))


def cmd_next_layer(args):
    state = load()
    if not state:
        return
    state["excavation_layer"] = min(state["excavation_layer"] + 1, 5)
    state["exchange_count"] = 0
    if state["excavation_layer"] >= 5:
        state["phase"] = "alignment"
    save(state)
    print(json.dumps({"layer": state["excavation_layer"], "phase": state["phase"]}))


def cmd_set_phase(args):
    state = load()
    if not state:
        return
    phase = args[0] if args else ""
    valid = ["excavation", "alignment", "architecture", "execution", "synthesis", "done"]
    if phase in valid:
        state["phase"] = phase
        state["exchange_count"] = 0
        save(state)
        print(json.dumps({"phase": phase}))
    else:
        print(json.dumps({"error": f"invalid phase: {phase}", "valid": valid}))


def cmd_list_modules(args):
    for mid, m in MODULES.items():
        print(f"  {mid:12s} | {m['name']:10s} | {m['purpose']} | Use when: {m['use_when']}")


def cmd_set_pipeline(args):
    state = load()
    if not state:
        return
    modules_str = args[0] if args else ""
    name = ""
    for i, a in enumerate(args):
        if a == "--name" and i + 1 < len(args):
            name = args[i + 1]
            break
    module_ids = [m.strip() for m in modules_str.split(",") if m.strip()]
    invalid = [m for m in module_ids if m not in MODULES]
    if invalid:
        print(json.dumps({"error": f"unknown modules: {invalid}"}))
        return
    state["pipeline"] = {
        "name": name or f"Pipeline ({','.join(module_ids)})",
        "modules": module_ids,
        "current_index": 0
    }
    save(state)
    print(json.dumps({"pipeline": state["pipeline"]["name"], "modules": module_ids}))


def cmd_current_module(args):
    state = load()
    if not state:
        return
    idx = state["pipeline"]["current_index"]
    modules = state["pipeline"]["modules"]
    if idx >= len(modules):
        print(json.dumps({"status": "done", "message": "All modules complete"}))
        return
    mid = modules[idx]
    m = MODULES[mid]
    print(json.dumps({
        "module_id": mid,
        "name": m["name"],
        "purpose": m["purpose"],
        "prompts": m["prompts"],
        "min_exchanges": m["exchanges"][0],
        "max_exchanges": m["exchanges"][1],
        "index": idx,
        "total": len(modules)
    }, ensure_ascii=False))


def cmd_save_module_output(args):
    state = load()
    if not state:
        return
    mid = args[0] if args else ""
    insights = " ".join(args[1:])
    state["module_outputs"][mid] = {
        "insights": insights.split("|") if "|" in insights else [insights],
        "timestamp": datetime.now().isoformat()
    }
    save(state)
    print(json.dumps({"saved": mid}))


def cmd_next_module(args):
    state = load()
    if not state:
        return
    state["pipeline"]["current_index"] += 1
    state["exchange_count"] = 0
    idx = state["pipeline"]["current_index"]
    total = len(state["pipeline"]["modules"])
    if idx >= total:
        state["phase"] = "synthesis"
    save(state)
    print(json.dumps({"index": idx, "total": total, "phase": state["phase"]}))


def cmd_archive(args):
    state = load()
    if not state:
        return
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    topic_slug = state["topic"][:30].replace(" ", "-").lower()
    archive_name = f"{ts}-{topic_slug}.json"
    dest = ARCHIVE_DIR / archive_name
    shutil.copy2(STATE_FILE, dest)
    STATE_FILE.unlink()
    print(json.dumps({"archived": str(dest)}))


def cmd_reset(args):
    if STATE_FILE.exists():
        STATE_FILE.unlink()
    print(json.dumps({"status": "reset"}))


def _current_module_name(state):
    idx = state["pipeline"]["current_index"]
    modules = state["pipeline"]["modules"]
    if not modules or idx >= len(modules):
        return "(none)"
    return MODULES.get(modules[idx], {}).get("name", modules[idx])


COMMANDS = {
    "init": cmd_init,
    "status": cmd_status,
    "get": cmd_get,
    "save-layer": cmd_save_layer,
    "next-layer": cmd_next_layer,
    "set-phase": cmd_set_phase,
    "list-modules": cmd_list_modules,
    "set-pipeline": cmd_set_pipeline,
    "current-module": cmd_current_module,
    "save-module-output": cmd_save_module_output,
    "next-module": cmd_next_module,
    "archive": cmd_archive,
    "reset": cmd_reset,
}


def main():
    if len(sys.argv) < 2:
        print("Usage: state.py <command> [args...]")
        print(f"Commands: {', '.join(COMMANDS.keys())}")
        sys.exit(1)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    if cmd in COMMANDS:
        COMMANDS[cmd](args)
    else:
        print(json.dumps({"error": f"unknown command: {cmd}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
