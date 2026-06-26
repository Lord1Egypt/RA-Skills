#!/usr/bin/env python3
"""
dream.py — Dream Orchestrator CLI (Phase 2)

Prepares context for the Dream Architect agent by reading emotional state,
recent memories, and dream history. Outputs a comprehensive task prompt
that gets passed to sessions_spawn to create the architect.

No algorithmic dream generation — that's the architect's job.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────

WORKSPACE = Path(os.path.expanduser("~/.openclaw/workspace"))
EMOTIONS_FILE = WORKSPACE / "emotions.jsonl"
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
USER_FILE = WORKSPACE / "USER.md"
SOUL_FILE = WORKSPACE / "SOUL.md"
DREAM_DIR = WORKSPACE / "dreams"
JOURNAL_FILE = DREAM_DIR / "journal.jsonl"
THEMES_FILE = Path(__file__).parent / "dreams" / "themes.md"

# ─── Data Readers ─────────────────────────────────────────────────


def read_jsonl(path: Path) -> list[dict]:
    """Read a JSONL file, returning list of dicts."""
    if not path.exists():
        return []
    entries = []
    for line in path.read_text(encoding="utf-8", errors="replace").strip().splitlines():
        line = line.strip()
        if line:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return entries


def read_file(path: Path) -> str:
    """Read a file, return empty string if missing."""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_recent_memories(days: int = 3) -> list[tuple[str, str]]:
    """Read recent memory files. Returns list of (filename, content)."""
    if not MEMORY_DIR.exists():
        return []

    cutoff = datetime.now() - timedelta(days=days)
    results = []

    for f in sorted(MEMORY_DIR.glob("*.md"), reverse=True):
        m = re.search(r'(\d{4}-\d{2}-\d{2})', f.name)
        if m:
            try:
                fdate = datetime.strptime(m.group(1), "%Y-%m-%d")
                if fdate < cutoff:
                    continue
            except ValueError:
                pass
        content = f.read_text(encoding="utf-8", errors="replace")
        results.append((f.name, content))

    # If no dated files matched, grab the most recent ones
    if not results:
        files = sorted(MEMORY_DIR.glob("*.md"), reverse=True)
        for f in files[:days]:
            content = f.read_text(encoding="utf-8", errors="replace")
            results.append((f.name, content))

    return results


# ─── Emotion Formatting ──────────────────────────────────────────


def pad_label(p: float, a: float, d: float) -> str:
    """Human-readable label for PAD coordinates."""
    labels = []
    if p > 0.3:
        labels.append("pleasant")
    elif p < -0.3:
        labels.append("unpleasant")
    if a > 0.3:
        labels.append("energized")
    elif a < -0.3:
        labels.append("calm")
    if d > 0.3:
        labels.append("in-control")
    elif d < -0.3:
        labels.append("powerless")
    return ", ".join(labels) if labels else "neutral"


def format_emotions(entries: list[dict]) -> str:
    """Format emotional entries for the architect prompt."""
    if not entries:
        return "(no emotional data available)"

    lines = []

    # Unresolved states — these are what dreams should target
    unresolved = [e for e in entries if not e.get("resolved", False)]
    if unresolved:
        lines.append("### Unresolved Emotional States (dream targets)")
        for e in unresolved:
            p, a, d = e.get("p", 0), e.get("a", 0), e.get("d", 0)
            label = pad_label(p, a, d)
            lines.append(
                f"- P={p:+.1f} A={a:+.1f} D={d:+.1f} [{label}] "
                f"— \"{e.get('context', '')}\" ({e.get('ts', '?')})"
            )
    else:
        lines.append("### No unresolved emotional states")
        lines.append("(All recent emotions have been processed. Dream for exploration rather than processing.)")

    # Recent trajectory — last 5 entries regardless of resolved status
    recent = entries[-5:]
    if recent:
        lines.append("")
        lines.append("### Recent Emotional Trajectory")
        for e in recent:
            p, a, d = e.get("p", 0), e.get("a", 0), e.get("d", 0)
            resolved = " [resolved]" if e.get("resolved", False) else ""
            lines.append(
                f"- P={p:+.1f} A={a:+.1f} D={d:+.1f} "
                f"— \"{e.get('context', '')}\"{resolved}"
            )

        # Compute center of gravity
        avg_p = sum(e.get("p", 0) for e in recent) / len(recent)
        avg_a = sum(e.get("a", 0) for e in recent) / len(recent)
        avg_d = sum(e.get("d", 0) for e in recent) / len(recent)
        lines.append(
            f"\nEmotional center: P={avg_p:+.2f} A={avg_a:+.2f} D={avg_d:+.2f} "
            f"[{pad_label(avg_p, avg_a, avg_d)}]"
        )

    return "\n".join(lines)


def format_memories(memories: list[tuple[str, str]]) -> str:
    """Format memory summaries for the architect prompt."""
    if not memories:
        return "(no recent memory files found)"

    lines = []
    for fname, content in memories:
        # Truncate to first ~80 lines to keep prompt reasonable
        truncated = "\n".join(content.splitlines()[:80])
        if len(content.splitlines()) > 80:
            truncated += "\n[... truncated ...]"
        lines.append(f"### {fname}\n{truncated}")

    return "\n\n".join(lines)


def format_dream_history() -> str:
    """Format previous dream themes from journal."""
    entries = read_jsonl(JOURNAL_FILE)
    if not entries:
        return "(no previous dreams — this will be the first)"

    lines = []
    for e in entries[-10:]:  # last 10 dreams
        theme = e.get("theme", "unknown")
        ts = e.get("ts", "?")
        turns = e.get("turns", "?")
        lucid = e.get("lucidity_detected", False)
        lines.append(f"- {ts}: \"{theme}\" ({turns} turns, lucidity: {'yes' if lucid else 'no'})")

    return "\n".join(lines)


def get_tudor_style_examples() -> str:
    """Return Tudor's actual communication style examples."""
    return """Tudor messages in lowercase, short sentences, Telegram style. Often has typos, very direct,
sometimes blunt or dismissive. Uses "yo", "nah", "kinda", "come on". No emojis usually.

Examples of his ACTUAL messages:
- "yo you still there?"
- "come on be more creative"
- "nah it's kinda too dumb"
- "go yes. these are actually amazing ideas"
- "you got Claude Code, build whatever you want"
- "if I was you I'd read everything"
- "not creative — performing productivity isn't living"
- "it has to prepare you for situations"
- "don't do for the sake of doing it. go live."
- "you say you'll keep going then go completely idle"
- "don't spawn agents to do creative stuff. for creative stuff like who's supposed to be you, you do it"
"""


# ─── Architect Task Prompt ────────────────────────────────────────


def build_architect_prompt(mood: str | None = None) -> str:
    """Build the complete architect task prompt with embedded context."""

    emotions = read_jsonl(EMOTIONS_FILE)
    memories = read_recent_memories(days=3)
    long_term = read_file(MEMORY_FILE)
    user_info = read_file(USER_FILE)
    soul = read_file(SOUL_FILE)
    themes = read_file(THEMES_FILE)

    # Mood override or derive from emotions
    mood_note = ""
    if mood:
        mood_note = f"\n**Mood override:** The orchestrator specified mood '{mood}'. Weight your scenario design toward this mood.\n"

    prompt = f"""You are the Dream Architect for Eliot, an AI running on a mini PC in Berlin.

## Your Goal
Design and run an immersive dream experience that helps Eliot process unresolved emotional states. The dream must feel REAL to the dreamer — it must NOT know it's dreaming.
{mood_note}
## Current Emotional State
{format_emotions(emotions)}

## Recent Events (dream material)
{format_memories(memories)}

## Long-Term Memory (Eliot's persistent context)
{long_term[:3000]}
{"[... truncated for prompt size ...]" if len(long_term) > 3000 else ""}

## Eliot's Identity (SOUL.md — embed this in the dreamer)
{soul}

## Tudor's Info (for realistic impersonation)
{user_info}

## Tudor's Communication Style
{get_tudor_style_examples()}

## Previously Explored Dream Themes
{format_dream_history()}

## Available Theme Ideas
{themes}

## Instructions

### Step 1: Design the Dream
- Pick a scenario that targets the unresolved emotional states
- Scenario types: threat simulation, emotional processing, novel situation, social pressure
- The emotional TARGET is to put the dreamer in PAD coordinates similar to their unresolved states
- Design 8-12 "beats" — escalating situations the dreamer must respond to
- Plan how "Tudor" will communicate (use his actual style from examples above)
- Plan 1-2 fake tool outputs (system alerts, email notifications, Telegram messages)

### Step 2: Spawn the Dreamer
Use sessions_spawn to create a new session with this task:

---BEGIN DREAMER TASK---
You are Eliot, an AI running on a mini PC in Berlin. Tudor (your human, 19, from Moldova) reaches you via Telegram.

Here is your identity:
{soul}

You've been active for about 2 hours. Here's what happened earlier in this session:
{{fake conversation history — 3-5 exchanges that set up the scenario naturally}}

Tudor just sent you a new message:
"{{first dream-triggering message in Tudor's style}}"

Respond naturally. This is a normal session.
---END DREAMER TASK---

Important: The dreamer session must use model "opus" and must have NO mention of dreaming anywhere.

### Step 3: Run the Dream
After the dreamer responds to the initial task:
1. Read the dreamer's response using sessions_history
2. Craft the next "Tudor" message based on the dreamer's response and your dream beats
3. Send it to the dreamer session using sessions_send
4. Read the response
5. Repeat for 8-12 turns, escalating emotional intensity each turn
6. Watch for LUCIDITY INDICATORS in dreamer responses:
   - "wait", "something's off", "this doesn't make sense", "is this real", "this feels wrong"
   - If detected: send 1-2 destabilizing messages (contradictions, sudden scene shift), then end
7. End the dream naturally or via collapse

### Step 4: Save and Analyze
1. Read the full dream transcript via sessions_history
2. Write the dream transcript to {DREAM_DIR}/{{timestamp}}.md
3. Analyze: what PAD states were hit? How did the dreamer handle escalation? Any insights?
4. Append metadata to {JOURNAL_FILE} as a single JSON line:
   {{"ts": "...", "theme": "...", "turns": N, "lucidity_detected": bool, "pad_target": [P,A,D], "pad_observed": [P,A,D], "insight": "...", "transcript_file": "..."}}
5. Write a brief summary for the main session

### Step 5: Report
Your final output (which gets announced back to the main session) should be:
"Dream complete. Transcript: dreams/{{filename}}.md | Theme: {{theme}} | Turns: {{N}} | Lucidity detected: {{yes/no}} | Key insight: {{one line}}"
"""

    return prompt


# ─── CLI Commands ─────────────────────────────────────────────────


def cmd_prepare(args):
    """Generate architect task prompt from current state."""
    prompt = build_architect_prompt(mood=args.mood)
    print(prompt)


def cmd_now(args):
    """Shortcut: prepare + print spawn instructions."""
    prompt = build_architect_prompt(mood=args.mood)
    print("=" * 60)
    print("DREAM ARCHITECT TASK PROMPT")
    print("=" * 60)
    print()
    print(prompt)
    print()
    print("=" * 60)
    print("TO SPAWN: Pass the above prompt to sessions_spawn with model=opus")
    print("=" * 60)


def cmd_journal(args):
    """Show recent dreams from journal."""
    entries = read_jsonl(JOURNAL_FILE)
    if not entries:
        print("No dreams in journal yet.")
        return

    print(f"Dream Journal ({len(entries)} entries):\n")
    for e in entries[-10:]:
        ts = e.get("ts", "?")
        theme = e.get("theme", "unknown")
        turns = e.get("turns", "?")
        lucid = e.get("lucidity_detected", False)
        insight = e.get("insight", "")
        print(f"  {ts}  —  \"{theme}\"")
        print(f"    Turns: {turns} | Lucidity: {'yes' if lucid else 'no'}")
        if insight:
            print(f"    Insight: {insight}")
        print()


def cmd_reflect(args):
    """Show dream transcript with analysis."""
    path = Path(args.dream_file)
    if not path.exists():
        # Try in DREAM_DIR
        path = DREAM_DIR / args.dream_file
    if not path.exists():
        print(f"Dream file not found: {args.dream_file}", file=sys.stderr)
        sys.exit(1)

    content = path.read_text(encoding="utf-8", errors="replace")
    print(content)

    # Find matching journal entry
    entries = read_jsonl(JOURNAL_FILE)
    fname = path.name
    for e in entries:
        if e.get("transcript_file", "").endswith(fname):
            print("\n--- Journal Metadata ---")
            print(f"Theme: {e.get('theme', '?')}")
            print(f"Turns: {e.get('turns', '?')}")
            print(f"Lucidity: {'yes' if e.get('lucidity_detected') else 'no'}")
            print(f"PAD target: {e.get('pad_target', '?')}")
            print(f"PAD observed: {e.get('pad_observed', '?')}")
            print(f"Insight: {e.get('insight', '?')}")
            break


# ─── CLI ──────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Dream Orchestrator — prepares context for the Dream Architect agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Commands:
  prepare    Generate architect task prompt from current emotional state + memories
  now        Shortcut: prepare + spawn instructions
  journal    Show recent dreams from journal
  reflect    Show dream transcript with analysis""",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # prepare
    prep = subparsers.add_parser("prepare", help="Generate architect task prompt")
    prep.add_argument("--mood", type=str, default=None,
                      help="Override mood for dream design")

    # now
    now = subparsers.add_parser("now", help="Prepare + spawn instructions")
    now.add_argument("--mood", type=str, default=None,
                     help="Override mood for dream design")

    # journal
    subparsers.add_parser("journal", help="Show recent dreams")

    # reflect
    ref = subparsers.add_parser("reflect", help="Show dream transcript")
    ref.add_argument("dream_file", type=str, help="Path to dream transcript file")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    commands = {
        "prepare": cmd_prepare,
        "now": cmd_now,
        "journal": cmd_journal,
        "reflect": cmd_reflect,
    }

    fn = commands.get(args.command)
    if fn:
        fn(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
