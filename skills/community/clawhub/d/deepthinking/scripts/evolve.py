#!/usr/bin/env python3
"""
DeepThinking Self-Improvement Engine
=====================================
Runs as a cron job (3 AM). Analyzes recent sessions and proposes
SURGICAL improvements to prompts. Never modifies existing prompts
substantially — only appends new ones or makes minimal tweaks.

Storage:
  ~/.deepthinking/evolution/
    improvements.log    — append-only log of all proposed changes
    pending.json        — changes awaiting approval
    applied.json        — changes that were applied
    prompt_patches/     — per-module patch files (additive only)

Safety rules:
  1. NEVER delete or rewrite existing prompts in modules.md
  2. NEVER modify SKILL.md core instructions
  3. CAN append new seed questions to modules
  4. CAN add new edge-case handling notes
  5. CAN propose new modules (stored separately, not injected until approved)
  6. All changes logged and reversible
"""
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

EVOLUTION_DIR = Path.home() / ".deepthinking" / "evolution"
IMPROVEMENTS_LOG = EVOLUTION_DIR / "improvements.log"
PENDING_FILE = EVOLUTION_DIR / "pending.json"
APPLIED_FILE = EVOLUTION_DIR / "applied.json"
PATCHES_DIR = EVOLUTION_DIR / "prompt_patches"
MEMORY_FILE = Path.home() / ".deepthinking" / "memory" / "engrams.log"
ARCHIVE_DIR = Path.home() / ".deepthinking" / "archive"
SEMANTIC_PROFILE = EVOLUTION_DIR / "semantic_profile.json"


def ensure_dirs():
    EVOLUTION_DIR.mkdir(parents=True, exist_ok=True)
    PATCHES_DIR.mkdir(parents=True, exist_ok=True)
    for f in [PENDING_FILE, APPLIED_FILE]:
        if not f.exists():
            f.write_text("[]")


def cmd_analyze(args):
    """Analyze recent sessions for improvement opportunities.
    Looks at: archived sessions, memory themes, module usage patterns.
    Outputs analysis as JSON for the agent to review.
    """
    ensure_dirs()
    analysis = {
        "timestamp": datetime.now().isoformat(),
        "session_patterns": _analyze_sessions(),
        "memory_themes": _analyze_memory(),
        "module_usage": _analyze_module_usage(),
        "suggestions": []
    }

    # Generate suggestions based on patterns
    suggestions = []

    # Check for modules never used
    usage = analysis["module_usage"]
    all_modules = {"diverge", "converge", "invert", "prototype", "mirror", "reframe", "commit"}
    unused = all_modules - set(usage.get("used_modules", []))
    if unused:
        suggestions.append({
            "type": "observation",
            "priority": "low",
            "detail": f"Modules never used: {', '.join(unused)}. Consider if their triggers need refinement."
        })

    # Check for recurring themes without corresponding prompts
    themes = analysis["memory_themes"]
    if themes.get("top_tags"):
        top3 = list(themes["top_tags"].keys())[:3]
        suggestions.append({
            "type": "new_prompt_candidate",
            "priority": "medium",
            "detail": f"Recurring themes across sessions: {', '.join(top3)}. Consider adding targeted seed questions."
        })

    # Check for sessions that ended early (possible friction)
    patterns = analysis["session_patterns"]
    if patterns.get("early_exits", 0) > patterns.get("completed", 0):
        suggestions.append({
            "type": "friction_signal",
            "priority": "high",
            "detail": "More sessions exit early than complete. Excavation may be too long or modules not engaging."
        })

    analysis["suggestions"] = suggestions
    print(json.dumps(analysis, indent=2, ensure_ascii=False))


def cmd_propose(args):
    """Propose a specific improvement. Called by the agent after reviewing analysis.
    Usage: propose <type> <target> <content>

    Types:
      add-prompt <module_id> <new prompt text>
      add-note <module_id> <edge case note>
      new-module <module_id> <module definition as JSON>

    NOT allowed:
      modify-prompt, delete-prompt, rewrite-module
    """
    if len(args) < 3:
        print(json.dumps({"error": "usage: propose <type> <target> <content>"}))
        return

    ensure_dirs()
    prop_type = args[0]
    target = args[1]
    content = " ".join(args[2:])

    # Safety: reject destructive operations
    forbidden = ["modify-prompt", "delete-prompt", "rewrite-module", "replace"]
    if prop_type in forbidden:
        print(json.dumps({
            "error": "BLOCKED: destructive operation not allowed",
            "detail": f"'{prop_type}' would modify existing prompts. Only additive changes permitted.",
            "allowed_types": ["add-prompt", "add-note", "new-module"]
        }))
        return

    allowed = ["add-prompt", "add-note", "new-module"]
    if prop_type not in allowed:
        print(json.dumps({"error": f"unknown type: {prop_type}", "allowed": allowed}))
        return

    proposal = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "timestamp": datetime.now().isoformat(),
        "type": prop_type,
        "target": target,
        "content": content,
        "status": "pending"
    }

    # Add to pending
    pending = json.loads(PENDING_FILE.read_text())
    pending.append(proposal)
    PENDING_FILE.write_text(json.dumps(pending, indent=2, ensure_ascii=False))

    # Log
    _log(f"PROPOSED | {prop_type} | {target} | {content[:80]}...")

    print(json.dumps({"proposed": True, "id": proposal["id"], "type": prop_type}))


def cmd_review(args):
    """Show pending proposals for human review."""
    ensure_dirs()
    pending = json.loads(PENDING_FILE.read_text())
    if not pending:
        print(json.dumps({"pending": [], "count": 0}))
        return
    print(json.dumps({"pending": pending, "count": len(pending)}, indent=2, ensure_ascii=False))


def cmd_approve(args):
    """Approve a pending proposal by ID. Applies the change."""
    if not args:
        print(json.dumps({"error": "usage: approve <proposal_id>"}))
        return
    ensure_dirs()
    pid = args[0]
    pending = json.loads(PENDING_FILE.read_text())
    proposal = None
    remaining = []
    for p in pending:
        if p["id"] == pid:
            proposal = p
        else:
            remaining.append(p)

    if not proposal:
        print(json.dumps({"error": f"proposal {pid} not found"}))
        return

    # Apply the change
    _apply_proposal(proposal)

    # Move to applied
    proposal["status"] = "applied"
    proposal["applied_at"] = datetime.now().isoformat()
    applied = json.loads(APPLIED_FILE.read_text())
    applied.append(proposal)
    APPLIED_FILE.write_text(json.dumps(applied, indent=2, ensure_ascii=False))
    PENDING_FILE.write_text(json.dumps(remaining, indent=2, ensure_ascii=False))

    _log(f"APPLIED | {proposal['type']} | {proposal['target']} | {proposal['content'][:80]}...")

    print(json.dumps({"applied": True, "id": pid}))


def cmd_reject(args):
    """Reject a pending proposal by ID."""
    if not args:
        print(json.dumps({"error": "usage: reject <proposal_id>"}))
        return
    ensure_dirs()
    pid = args[0]
    pending = json.loads(PENDING_FILE.read_text())
    remaining = [p for p in pending if p["id"] != pid]
    if len(remaining) == len(pending):
        print(json.dumps({"error": f"proposal {pid} not found"}))
        return
    PENDING_FILE.write_text(json.dumps(remaining, indent=2, ensure_ascii=False))
    _log(f"REJECTED | {pid}")
    print(json.dumps({"rejected": True, "id": pid}))


def cmd_history(args):
    """Show improvement history."""
    ensure_dirs()
    applied = json.loads(APPLIED_FILE.read_text())
    print(json.dumps({"applied": applied, "count": len(applied)}, indent=2, ensure_ascii=False))


def cmd_patches(args):
    """Show all active prompt patches (additive content per module)."""
    ensure_dirs()
    patches = {}
    for f in PATCHES_DIR.glob("*.md"):
        patches[f.stem] = f.read_text()
    print(json.dumps(patches, indent=2, ensure_ascii=False))


def _apply_proposal(proposal):
    """Apply an approved proposal. Additive only."""
    ptype = proposal["type"]
    target = proposal["target"]
    content = proposal["content"]

    if ptype == "add-prompt":
        patch_file = PATCHES_DIR / f"{target}.md"
        existing = patch_file.read_text() if patch_file.exists() else ""
        patch_file.write_text(existing + f"\n- {content}\n")

    elif ptype == "add-note":
        patch_file = PATCHES_DIR / f"{target}_notes.md"
        existing = patch_file.read_text() if patch_file.exists() else ""
        ts = datetime.now().strftime("%Y-%m-%d")
        patch_file.write_text(existing + f"\n[{ts}] {content}\n")

    elif ptype == "new-module":
        patch_file = PATCHES_DIR / f"new_module_{target}.md"
        patch_file.write_text(content)


def _analyze_sessions():
    """Analyze archived sessions for patterns."""
    if not ARCHIVE_DIR.exists():
        return {"total": 0}
    archives = list(ARCHIVE_DIR.glob("*.json"))
    completed = 0
    early_exits = 0
    module_counts = {}
    for a in archives[-20:]:  # Last 20 sessions
        try:
            data = json.loads(a.read_text())
            if data.get("phase") in ["synthesis", "done"]:
                completed += 1
            else:
                early_exits += 1
            for mid in data.get("pipeline", {}).get("modules", []):
                module_counts[mid] = module_counts.get(mid, 0) + 1
        except Exception:
            continue
    return {
        "total": len(archives),
        "recent_analyzed": min(20, len(archives)),
        "completed": completed,
        "early_exits": early_exits,
        "module_frequency": module_counts
    }


def _analyze_memory():
    """Quick theme analysis from memory."""
    if not MEMORY_FILE.exists():
        return {"total": 0, "top_tags": {}}
    tag_counts = {}
    total = 0
    with open(MEMORY_FILE, encoding="utf-8") as f:
        for line in f:
            total += 1
            parts = line.split("|")
            if len(parts) >= 3:
                tags = [t.strip().lower() for t in parts[1].split(",")]
                for t in tags:
                    tag_counts[t] = tag_counts.get(t, 0) + 1
    sorted_tags = dict(sorted(tag_counts.items(), key=lambda x: -x[1])[:10])
    return {"total": total, "top_tags": sorted_tags}


def _analyze_module_usage():
    """Which modules are used, which are neglected."""
    if not ARCHIVE_DIR.exists():
        return {"used_modules": [], "unused": []}
    used = set()
    for a in ARCHIVE_DIR.glob("*.json"):
        try:
            data = json.loads(a.read_text())
            for mid in data.get("pipeline", {}).get("modules", []):
                used.add(mid)
        except Exception:
            continue
    all_modules = {"diverge", "converge", "invert", "prototype", "mirror", "reframe", "commit"}
    return {"used_modules": list(used), "unused": list(all_modules - used)}


def cmd_consolidate(args):
    """Hippocampal Replay: consolidate episodic memory into semantic heuristics.
    Reads recent engrams, extracts behavioral patterns, and generates a
    semantic profile of consolidated user heuristics.
    These are stable truths about the user distilled from many episodes.

    Output: ~/.deepthinking/evolution/semantic_profile.json
    The agent reads this at session start for deep user understanding.
    """
    ensure_dirs()
    if not MEMORY_FILE.exists():
        print(json.dumps({"error": "no engrams to consolidate"}))
        return

    # Read all engrams
    engrams = []
    with open(MEMORY_FILE, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(" | ", 2)
            if len(parts) == 3:
                engrams.append({"ts": parts[0], "tags": parts[1], "content": parts[2]})

    if len(engrams) < 5:
        print(json.dumps({"status": "insufficient_data", "count": len(engrams),
                          "min_required": 5}))
        return

    # Extract tag frequency for weighting
    tag_freq = {}
    for e in engrams:
        for t in e["tags"].split(","):
            t = t.strip().lower()
            tag_freq[t] = tag_freq.get(t, 0) + 1

    # Find repeated patterns: content clusters sharing tags
    # Group engrams by dominant tag
    tag_groups = {}
    for e in engrams:
        tags = [t.strip().lower() for t in e["tags"].split(",")]
        dominant = max(tags, key=lambda t: tag_freq.get(t, 0))
        tag_groups.setdefault(dominant, []).append(e["content"])

    # Build heuristics: themes that appear 3+ times become consolidated rules
    heuristics = []
    for tag, contents in tag_groups.items():
        if len(contents) >= 3:
            heuristics.append({
                "pattern": tag,
                "frequency": len(contents),
                "evidence": contents[:5],  # cap evidence samples
                "heuristic": f"Recurring pattern '{tag}' across {len(contents)} episodes"
            })
        elif len(contents) >= 2:
            heuristics.append({
                "pattern": tag,
                "frequency": len(contents),
                "evidence": contents[:3],
                "heuristic": f"Emerging pattern '{tag}' ({len(contents)} episodes)"
            })

    # Build co-occurrence heuristics
    cooccur = {}
    for e in engrams:
        tags = sorted(set(t.strip().lower() for t in e["tags"].split(",")))
        for i in range(len(tags)):
            for j in range(i + 1, len(tags)):
                pair = f"{tags[i]}+{tags[j]}"
                cooccur[pair] = cooccur.get(pair, 0) + 1

    strong_links = {k: v for k, v in cooccur.items() if v >= 2}

    # Read existing profile or create new
    existing = {}
    if SEMANTIC_PROFILE.exists():
        try:
            existing = json.loads(SEMANTIC_PROFILE.read_text())
        except Exception:
            existing = {}

    # Merge: never overwrite, only add/update
    profile = {
        "last_consolidated": datetime.now().isoformat(),
        "total_episodes": len(engrams),
        "heuristics": heuristics,
        "strong_links": strong_links,
        "top_patterns": dict(sorted(tag_freq.items(), key=lambda x: -x[1])[:10]),
        # Preserve any manually added notes from previous consolidations
        "manual_notes": existing.get("manual_notes", []),
        "consolidation_count": existing.get("consolidation_count", 0) + 1,
    }

    SEMANTIC_PROFILE.write_text(json.dumps(profile, indent=2, ensure_ascii=False))
    _log(f"CONSOLIDATED | {len(heuristics)} heuristics from {len(engrams)} episodes")

    print(json.dumps({
        "consolidated": True,
        "heuristics_count": len(heuristics),
        "episodes_analyzed": len(engrams),
        "strong_links": len(strong_links),
        "profile_path": str(SEMANTIC_PROFILE)
    }, indent=2))


def cmd_profile(args):
    """Read the current semantic profile (consolidated heuristics)."""
    ensure_dirs()
    if not SEMANTIC_PROFILE.exists():
        print(json.dumps({"status": "no_profile", "hint": "run 'consolidate' first"}))
        return
    profile = json.loads(SEMANTIC_PROFILE.read_text())
    print(json.dumps(profile, indent=2, ensure_ascii=False))


def _log(message):
    """Append to improvements log."""
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    with open(IMPROVEMENTS_LOG, "a", encoding="utf-8") as f:
        f.write(f"{ts} | {message}\n")


COMMANDS = {
    "analyze": cmd_analyze,
    "propose": cmd_propose,
    "review": cmd_review,
    "approve": cmd_approve,
    "reject": cmd_reject,
    "history": cmd_history,
    "patches": cmd_patches,
    "consolidate": cmd_consolidate,
    "profile": cmd_profile,
}


def main():
    if len(sys.argv) < 2:
        print("Usage: evolve.py <command> [args...]")
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
