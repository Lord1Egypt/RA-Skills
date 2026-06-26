#!/usr/bin/env python3
"""
DeepThinking TUI
================
Standalone terminal user interface for the DeepThinking cognitive framework.
Runs on any VPS/server via SSH. No external dependencies — pure stdlib.

Usage:
  python3 scripts/tui.py [topic]
  ./bin/deep "I want to start a business"
  ./bin/deep          (resume existing session)
"""

import json
import os
import sys
import subprocess
import readline
import textwrap
from pathlib import Path

# ─── ANSI Color System ────────────────────────────────────────────────────────

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    ITALIC  = "\033[3m"

    # Text colors
    WHITE   = "\033[97m"
    GRAY    = "\033[90m"
    SILVER  = "\033[37m"
    CYAN    = "\033[96m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    YELLOW  = "\033[93m"
    GREEN   = "\033[92m"
    RED     = "\033[91m"

    # Background
    BG_DARK = "\033[48;5;235m"

def bold(s):    return f"{C.BOLD}{s}{C.RESET}"
def dim(s):     return f"{C.DIM}{C.GRAY}{s}{C.RESET}"
def cyan(s):    return f"{C.CYAN}{s}{C.RESET}"
def blue(s):    return f"{C.BLUE}{s}{C.RESET}"
def magenta(s): return f"{C.MAGENTA}{s}{C.RESET}"
def yellow(s):  return f"{C.YELLOW}{s}{C.RESET}"
def green(s):   return f"{C.GREEN}{s}{C.RESET}"
def red(s):     return f"{C.RED}{s}{C.RESET}"
def gray(s):    return f"{C.GRAY}{s}{C.RESET}"
def white(s):   return f"{C.WHITE}{C.BOLD}{s}{C.RESET}"

# ─── Layout Helpers ───────────────────────────────────────────────────────────

TERM_WIDTH = min(os.get_terminal_size().columns if sys.stdout.isatty() else 80, 90)

def ruler(char="─", color=C.GRAY):
    print(f"{color}{char * TERM_WIDTH}{C.RESET}")

def section(title, color=C.CYAN):
    print()
    ruler("─", color)
    print(f"{color}{C.BOLD} {title}{C.RESET}")
    ruler("─", color)
    print()

def wrap_print(text, indent=2, width=None):
    w = (width or TERM_WIDTH) - indent
    prefix = " " * indent
    for line in textwrap.wrap(text, width=w):
        print(f"{prefix}{line}")

def agent_say(text):
    """Agent's voice — the main conversational output."""
    print()
    prefix = f"  {cyan('◆')}  "
    w = TERM_WIDTH - 6
    lines = textwrap.wrap(text, width=w)
    for i, line in enumerate(lines):
        if i == 0:
            print(f"{prefix}{C.WHITE}{line}{C.RESET}")
        else:
            print(f"      {C.WHITE}{line}{C.RESET}")
    print()

def agent_aside(text):
    """Subtle system message — lower priority."""
    print(f"  {dim('·')}  {dim(text)}")

def phase_banner(phase_name, color=C.CYAN):
    print()
    label = f"  PHASE: {phase_name.upper()}  "
    bar = "━" * len(label)
    print(f"  {color}{C.BOLD}{bar}{C.RESET}")
    print(f"  {color}{C.BOLD}{label}{C.RESET}")
    print(f"  {color}{C.BOLD}{bar}{C.RESET}")
    print()

def prompt_input(hint="you"):
    """Read user input with a styled prompt."""
    try:
        raw = input(f"  {gray('›')} {C.WHITE}")
    except (EOFError, KeyboardInterrupt):
        print(C.RESET)
        return "/deepend"
    finally:
        print(C.RESET, end="")
    return raw.strip()

# ─── Script Runner ─────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent.parent

def run_script(script, *args):
    """Run a DeepThinking sub-script and return parsed JSON output."""
    cmd = [sys.executable, str(BASE_DIR / "scripts" / script)] + list(str(a) for a in args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.stdout.strip():
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {"raw": result.stdout.strip()}
        return {}
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    except Exception as e:
        return {"error": str(e)}

def state(*args):
    return run_script("state.py", *args)

def memory(*args):
    return run_script("memory.py", *args)

def evolve(*args):
    return run_script("evolve.py", *args)

# ─── Excavation Phase ─────────────────────────────────────────────────────────

EXCAVATION_QUESTIONS = [
    # Layer 0 — Surface
    lambda topic: f"Tell me more. What does \"{topic}\" actually look like in your head?",
    # Layer 1 — Context
    lambda _: "What's happening in your life right now that made this come up?",
    # Layer 2 — Energy
    lambda _: "When you imagine yourself a year from now, doing this full-time — what part gives you energy? What part feels like homework?",
    # Layer 3 — Fear
    lambda _: "What's the worst case in your head? Not the logical one. The one you don't say out loud.",
    # Layer 4 — Real Want (crafted dynamically)
    None,
]

def run_excavation(session):
    phase_banner("Excavation", C.BLUE)
    agent_aside("Five questions. One at a time. Go as deep as you want.")
    print()

    topic = session.get("topic", "")
    profile = session.get("profile", {})
    start_layer = session.get("excavation_layer", 0)

    layers_data = {
        0: profile.get("surface_ask", ""),
        1: profile.get("life_context", ""),
        2: profile.get("energy_map", ""),
        3: profile.get("fear", ""),
        4: profile.get("real_want", ""),
    }

    for layer in range(start_layer, 5):
        if layer < 4:
            question = EXCAVATION_QUESTIONS[layer](topic)
        else:
            # Layer 4: craft based on gap
            gap = _detect_gap(layers_data)
            question = gap

        agent_say(question)

        user_input = prompt_input()
        if user_input.lower() in ("/deepend", "/deepend", "exit", "quit"):
            return "exit"

        layers_data[layer] = user_input
        state("save-layer", str(layer), user_input)
        state("next-layer")

        # Store engram
        tag_map = {0: "input,topic", 1: "context,life", 2: "energy,motivation", 3: "fear", 4: "want,core"}
        tags = tag_map.get(layer, "insight")
        memory("store", tags, user_input[:200])

        # Small breath between layers
        if layer < 4:
            print()
            agent_aside(f"Layer {layer + 1}/5 saved.")

    return "done"


def _detect_gap(layers):
    surface = layers.get(0, "")
    fear = layers.get(3, "")
    if fear and len(fear) > 20:
        return f"Here's what I'm noticing: you said you want {surface[:60].lower()}... but what you described as your fear tells a different story. What do you actually want — not what you should want?"
    return "Put aside what's practical for a second. If everything worked out exactly right, what would your version of success actually feel like day-to-day?"

# ─── Alignment Phase ──────────────────────────────────────────────────────────

def run_alignment(session):
    phase_banner("Alignment", C.MAGENTA)

    profile = state("get", "profile")
    surface = profile.get("surface_ask", "")
    context = profile.get("life_context", "")
    energy = profile.get("energy_map", "")
    fear = profile.get("fear", "")
    real_want = profile.get("real_want", "")

    read = (
        f"Here's what I'm hearing. Tell me if I'm wrong:\n\n"
        f"You want {surface[:80]}, but what's driving this is something deeper — "
        f"probably connected to {context[:60] if context else 'where you are right now'}.\n\n"
        f"The thing that gives you energy: {energy[:80] if energy else 'something specific you described'}.\n\n"
        f"What you're actually afraid of isn't failure — it's {fear[:80] if fear else 'something harder to name'}.\n\n"
        f"What you really need isn't just an answer. It's {real_want[:80] if real_want else 'clarity on the real question'}.\n\n"
        f"Am I close?"
    )

    agent_say(read)

    user_input = prompt_input()
    if user_input.lower() in ("/deepend", "exit"):
        return "exit"

    lower = user_input.lower()
    if any(w in lower for w in ["yes", "sim", "yeah", "exactly", "correct", "certo", "isso"]):
        state("set-phase", "architecture")
        memory("store", "alignment,confirmed", f"User confirmed alignment on topic: {surface[:100]}")
        return "confirmed"
    else:
        # Store correction
        state("save-layer", "4", user_input)
        memory("store", "alignment,correction", user_input[:200])
        agent_say("Got it. Let me adjust...")
        return "corrected"

# ─── Architecture Phase ───────────────────────────────────────────────────────

MODULE_LOGIC = {
    "diverge":   "Can't see the options",
    "converge":  "Too many options",
    "invert":    "Too attached to one idea",
    "prototype": "Stuck in abstraction",
    "mirror":    "Orbiting the same theme",
    "reframe":   "Solving the wrong problem",
    "commit":    "Has clarity but won't act",
}

def run_architecture(session):
    phase_banner("Architecture", C.YELLOW)

    profile = state("get", "profile")
    fear = profile.get("fear", "")
    real_want = profile.get("real_want", "")
    energy = profile.get("energy_map", "")

    # Select modules heuristically
    pipeline = []

    # Always start with a diagnostic
    if "don't know" in real_want.lower() or "não sei" in real_want.lower():
        pipeline.append("diverge")
    elif "too many" in real_want.lower() or "muitas" in real_want.lower():
        pipeline.append("converge")
    else:
        pipeline.append("diverge")

    # Fear-based additions
    if fear and len(fear) > 10:
        pipeline.append("invert")
        pipeline.append("mirror")
    else:
        pipeline.append("mirror")

    # Energy-based closer
    if "practical" in energy.lower() or "action" in energy.lower() or "fazer" in energy.lower():
        pipeline.append("prototype")
    pipeline.append("commit")

    # Deduplicate, cap at 4
    seen = set()
    final = []
    for m in pipeline:
        if m not in seen:
            seen.add(m)
            final.append(m)
    final = final[:4]

    # Present the plan
    agent_say(f"I built a custom pipeline for you. Here's the plan:\n")
    for i, mod in enumerate(final, 1):
        mod_data = _get_module_data(mod)
        use_when_label = dim(f"Use when: {mod_data['use_when']}")
        print(f"  {yellow(f'Phase {i}:')} {bold(mod_data['name'])} — {mod_data['purpose']}")
        print(f"    {use_when_label}")
        print()

    agent_say("Not rigid. We adapt as we go. About 4-6 exchanges per phase.\n\nReady?")

    user_input = prompt_input()
    if user_input.lower() in ("/deepend", "exit"):
        return "exit"

    # Save pipeline
    state("set-pipeline", ",".join(final), "--name", "Custom Pipeline v1")
    state("set-phase", "execution")

    return "ready"


def _get_module_data(mod_id):
    """Get module info from state.py output."""
    # Use state.py list-modules or inline our local copy
    modules = {
        "diverge":   {"name": "Diverge",   "purpose": "Generate possibilities without judgment", "use_when": "Stuck on one path"},
        "converge":  {"name": "Converge",  "purpose": "Filter with criteria. Kill options ruthlessly.", "use_when": "Too many options"},
        "invert":    {"name": "Invert",    "purpose": "Stress-test. Pre-mortem. Steelman the opposite.", "use_when": "Too attached to one idea"},
        "prototype": {"name": "Prototype", "purpose": "Make it concrete. 48 hours, $0.", "use_when": "Stuck in abstraction"},
        "mirror":    {"name": "Mirror",    "purpose": "Reflect patterns the user can't see.", "use_when": "Orbiting same theme"},
        "reframe":   {"name": "Reframe",   "purpose": "Change the problem entirely.", "use_when": "Solving the wrong problem"},
        "commit":    {"name": "Commit",    "purpose": "Force decision. First action. Deadline.", "use_when": "Has clarity but won't act"},
    }
    return modules.get(mod_id, {"name": mod_id, "purpose": "?", "use_when": "?"})

# ─── Execution Phase ──────────────────────────────────────────────────────────

def run_execution(session):
    phase_banner("Execution", C.CYAN)

    while True:
        mod_info = state("current-module")
        if mod_info.get("status") == "done":
            break

        mod_id   = mod_info.get("module_id", "")
        mod_name = mod_info.get("name", mod_id)
        prompts  = mod_info.get("prompts", [])
        idx      = mod_info.get("index", 0)
        total    = mod_info.get("total", 1)

        section(f"Module {idx+1}/{total}: {mod_name}", C.CYAN)
        agent_aside(mod_info.get("purpose", ""))
        print()

        # Also load any evolved patches for this module
        patches = evolve("patches")
        extra_prompts = []
        if isinstance(patches, dict) and mod_id in patches:
            patch_text = patches[mod_id]
            extra_prompts = [line.lstrip("- ").strip() for line in patch_text.splitlines() if line.strip().startswith("-")]

        all_prompts = prompts + extra_prompts
        insights = []
        prompt_index = 0
        exchanges = 0
        min_ex = mod_info.get("min_exchanges", 3)

        while prompt_index < len(all_prompts):
            q = all_prompts[prompt_index]
            agent_say(q)
            prompt_index += 1

            user_input = prompt_input()
            if user_input.lower() in ("/deepend", "exit"):
                return "exit"
            if user_input.lower() in ("next", "done", "proximo", "próximo", "fim"):
                break

            exchanges += 1
            insights.append(user_input[:150])

            # Store engram from key exchanges
            if exchanges % 2 == 0 or exchanges == 1:
                memory("store", f"{mod_id},execution", user_input[:200])

            # Push back on lazy answers
            lazy_signals = ["not sure", "maybe", "i don't know", "não sei", "talvez", "depende"]
            if any(s in user_input.lower() for s in lazy_signals) and exchanges < 3:
                agent_say("That sounds like a warm-up answer. What's the real one?")
                user_input2 = prompt_input()
                if user_input2.lower() not in ("/deepend", "exit"):
                    insights.append(user_input2[:150])
                    memory("store", f"{mod_id},breakthrough", user_input2[:200])

            # Celebrate breakthroughs
            if len(user_input) > 100 and any(w in user_input.lower() for w in ["realize", "percebi", "actually", "na verdade"]):
                print()
                agent_aside("Yeah. Write that down.")
                print()

            if exchanges >= min_ex and prompt_index >= len(all_prompts):
                break

        # Save module output
        pipe_insights = " | ".join(insights[:3]) if insights else "no insights captured"
        state("save-module-output", mod_id, pipe_insights)
        state("next-module")

        print()
        agent_aside(f"✓ {mod_name} complete.")
        print()

    return "done"

# ─── Synthesis Phase ──────────────────────────────────────────────────────────

def run_synthesis(session):
    phase_banner("Synthesis", C.GREEN)

    profile = state("get", "profile")
    outputs = state("get", "outputs")

    topic   = session.get("topic", "your question")
    surface = profile.get("surface_ask", "")
    fear    = profile.get("fear", "")
    want    = profile.get("real_want", "")

    # Build synthesis from outputs
    module_insights = []
    if isinstance(outputs, dict):
        for mod_id, out in outputs.items():
            if isinstance(out, dict):
                insigs = out.get("insights", [])
                if insigs:
                    module_insights.extend(insigs[:2])

    fear_fallback      = "what you're afraid of"
    next_fallback      = "Whatever you said you'd do — start with that one thing."
    tension_part       = fear[:60] if fear else fear_fallback
    surprise_part      = module_insights[0] if module_insights else want
    next_move_part     = module_insights[-1] if len(module_insights) > 1 else next_fallback

    agent_say(
        f"Here's what came out of this session on \"{topic}\".\n\n"
        f"You came in asking about {surface[:60]}. What emerged is different: "
        f"the real tension is between what you want and {tension_part}.\n\n"
        f"The thing that surprised me: {surprise_part}.\n\n"
        f"Your next move: {next_move_part}.\n\n"
        f"What I'd push back on: don't mistake clarity here for a decision made. "
        f"The real test is what you do in the next 48 hours."
    )

    # Store core engram
    core_insight = module_insights[0] if module_insights else want
    memory("store", "synthesis,core", core_insight[:200])

    print()
    agent_say("Want me to:\n  1. Save this as a document\n  2. Build a 7-day action plan\n  3. Keep exploring a thread\n  4. End here")

    choice = prompt_input()

    if "1" in choice or "document" in choice.lower() or "salvar" in choice.lower():
        _save_synthesis_doc(session, profile, module_insights)
    elif "2" in choice or "plan" in choice.lower() or "plano" in choice.lower():
        _build_action_plan(module_insights)
    elif "3" in choice or "explor" in choice.lower():
        agent_say("Which thread? Tell me what's still pulling at you.")
        prompt_input()  # let them express, then end
    else:
        agent_say("Good session. State archived.")

    state("archive")
    return "done"


def _save_synthesis_doc(session, profile, insights):
    from datetime import datetime
    out_dir = Path.home() / ".deepthinking" / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M")
    topic_slug = session.get("topic", "session")[:30].replace(" ", "-").lower()
    out_file = out_dir / f"{ts}-{topic_slug}.md"

    lines = [
        f"# DeepThinking Session: {session.get('topic', '')}",
        f"*{datetime.now().strftime('%B %d, %Y')}*\n",
        "## What You Came In With",
        profile.get("surface_ask", ""),
        "\n## What Emerged",
    ] + [f"- {i}" for i in insights] + [
        "\n## Your Next Move",
        insights[-1] if insights else "—",
    ]

    out_file.write_text("\n".join(lines))
    agent_aside(f"Saved → {out_file}")


def _build_action_plan(insights):
    agent_say("7-Day Action Plan:\n")
    days = ["Today", "Day 2", "Day 3", "Day 5", "Day 7"]
    for i, day in enumerate(days):
        if i < len(insights):
            print(f"  {yellow(day+':')} {insights[i][:80]}")
        else:
            print(f"  {dim(day+':')} {dim('Your call.')}")
    print()

# ─── Main Loop ────────────────────────────────────────────────────────────────

def print_header():
    ruler("═", C.CYAN)
    print(f"\n  {C.CYAN}{C.BOLD}◆  DeepThinking{C.RESET}  {dim('stateful cognitive framework')}")
    print(f"  {dim('Commands: /deepend to pause · /deep to resume · Ctrl+C to quit')}\n")
    ruler("═", C.CYAN)

def main():
    print_header()

    # Determine topic
    topic_arg = " ".join(sys.argv[1:]).strip()

    # Check existing session
    session_status = state("status")

    if session_status.get("status") == "no_session":
        if not topic_arg:
            print()
            agent_say("What would you like to explore?")
            topic_arg = prompt_input()
            if topic_arg.lower() in ("/deepend", "exit", ""):
                print()
                agent_aside("Nothing started. Come back anytime.")
                return

        agent_aside(f"Starting new session: \"{topic_arg}\"")
        state("init", "--topic", topic_arg)
        session_data = state("status")

        # Load profile silently
        evo_profile = evolve("profile")
        if evo_profile.get("status") != "no_profile":
            agent_aside("Profile loaded.")

        # Search memory for related context
        keywords = " ".join(topic_arg.split()[:3])
        mem_results = memory("search", keywords)
        # (silently absorbed — not announced to user)

    else:
        topic_arg = session_status.get("topic", "existing session")
        phase = session_status.get("phase", "excavation")
        agent_aside(f"Resuming: \"{topic_arg}\" — phase: {phase}")
        session_data = session_status

    # ── Phase Loop ──
    while True:
        session_data = state("status")
        phase = session_data.get("phase", "excavation")

        if phase == "excavation":
            result = run_excavation(session_data)
            if result == "exit":
                _handle_exit(session_data)
                return

        elif phase == "alignment":
            result = run_alignment(session_data)
            if result == "exit":
                _handle_exit(session_data)
                return

        elif phase == "architecture":
            result = run_architecture(session_data)
            if result == "exit":
                _handle_exit(session_data)
                return

        elif phase == "execution":
            result = run_execution(session_data)
            if result == "exit":
                _handle_exit(session_data)
                return

        elif phase == "synthesis":
            run_synthesis(session_data)
            print()
            ruler("═", C.CYAN)
            print(f"\n  {green('◆')} {bold('Session complete.')}")
            print(f"  {dim('Start a new one anytime with: ./bin/deep')}\n")
            ruler("═", C.CYAN)
            return

        else:
            agent_aside(f"Unknown phase: {phase}")
            return


def _handle_exit(session_data):
    print()
    ruler("─", C.GRAY)
    agent_say(
        "Pausing here. State saved.\n\n"
        "One thing to sit with: what you said about your fear — that's the real thread.\n\n"
        "Pick up anytime: ./bin/deep"
    )
    ruler("─", C.GRAY)
    print()


if __name__ == "__main__":
    main()
