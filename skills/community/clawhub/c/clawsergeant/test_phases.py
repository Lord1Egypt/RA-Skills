"""Step-by-step testing for each phase of the ClawSergeant pipeline.

Usage:
    python test_phases.py 1          # Phase 1: test LLM connection
    python test_phases.py 2          # Phase 2: test curriculum generation
    python test_phases.py 3          # Phase 3: test Claw agent communication
    python test_phases.py 4          # Phase 4: single-task training round
    python test_phases.py all        # Run all phases sequentially
"""

import asyncio
import json
import logging
import os
import sys

from dotenv import load_dotenv
from loguru import logger


class _InterceptHandler(logging.Handler):
    """Route standard-library logging (used by httpx etc.) through loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        logger.opt(depth=6, exception=record.exc_info).log(
            level, record.getMessage()
        )


logger.remove()
logger.add(sys.stderr, level="INFO")
logging.basicConfig(handlers=[_InterceptHandler()], level=0, force=True)


def _env_setup() -> tuple[str, str, str, str]:
    """Load .env and return (api_key, base_url, model, recipient)."""
    load_dotenv()
    api_key = os.getenv("LLM_API_KEY", "")
    base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("LLM_MODEL", "gpt-4o")
    recipient = os.getenv("CLAW_RECIPIENT", "")
    return api_key, base_url, model, recipient


# ── Phase 1: LLM connectivity ────────────────────────────────────────────────

async def phase1_llm_connection():
    """Verify that the LLM API is reachable and responds."""
    from llm_handler import LLMHandler, Conversation

    api_key, base_url, model, *_ = _env_setup()
    if not api_key:
        sys.exit("[FAIL] LLM_API_KEY not set in .env")

    print(f"\n=== Phase 1: LLM Connection Test ===")
    print(f"Base URL : {base_url}")
    print(f"Model    : {model}")

    llm = LLMHandler(api_key=api_key, base_url=base_url, model=model)
    await llm.start()
    try:
        conv = Conversation(system_prompt="You are a helpful assistant.")
        conv.add("user", "Reply with exactly: CONNECTION_OK")
        reply = await llm.chat(conv, temperature=0.0)
        print(f"Reply    : {reply}")
        if "CONNECTION_OK" in reply.upper():
            print("[PASS] LLM connection works.\n")
        else:
            print("[WARN] Got a reply but content unexpected — check model.\n")
    finally:
        await llm.stop()


# ── Phase 2: Curriculum generation ────────────────────────────────────────────

async def phase2_curriculum():
    """Generate a curriculum from a test intent and display the result."""
    from llm_handler import LLMHandler
    from curriculum import design_curriculum

    api_key, base_url, model, *_ = _env_setup()
    if not api_key:
        sys.exit("[FAIL] LLM_API_KEY not set in .env")

    print(f"\n=== Phase 2: Curriculum Generation Test ===")

    test_intent = "A rigorous and efficient programming assistant"
    print(f"Test intent: \"{test_intent}\"")
    print("Generating curriculum (this may take 10-30s)...")

    llm = LLMHandler(api_key=api_key, base_url=base_url, model=model)
    await llm.start()
    try:
        curriculum = await design_curriculum(llm, test_intent)

        print(f"\nTitle   : {curriculum.title}")
        print(f"Overview: {curriculum.overview}")
        print(f"Target  : {curriculum.target_persona}")
        print(f"Stages  : {len(curriculum.stages)}")
        for stage in curriculum.stages:
            print(f"  [{stage.id}] {stage.name}")
            for t in stage.tasks:
                print(f"       Task {t.task_id}: {t.description}")
            for c in stage.evaluation_criteria:
                print(f"       Eval: {c.criterion} -> {c.passing_standard}")

        if curriculum.stages:
            print("\n[PASS] Curriculum generated successfully.\n")
        else:
            print("\n[FAIL] Curriculum has no stages.\n")

        return curriculum
    finally:
        await llm.stop()


# ── Phase 3: Claw agent communication ────────────────────────────────────────

async def phase3_claw_agent():
    """Send a test message to the Claw agent and display the reply."""
    from claw_agent import ClawAgent

    *_, recipient = _env_setup()
    if not recipient:
        sys.exit("[FAIL] CLAW_RECIPIENT not set in .env")

    print(f"\n=== Phase 3: Claw Agent Communication Test ===")
    print(f"Recipient : {recipient}")

    agent = ClawAgent(recipient=recipient)
    test_msg = (
        "This is a connectivity test from ClawSergeant. "
        "Please reply with a brief confirmation."
    )
    print(f"Sending   : \"{test_msg}\"")

    reply = await agent.send(test_msg)
    print(f"Reply     : {reply}")
    print("[PASS] Claw agent communication works.\n")
    return reply


# ── Phase 4: Single-task training round ──────────────────────────────────────

async def phase4_single_task():
    """Run one training task: trainer LLM -> Claw agent -> evaluator LLM."""
    from llm_handler import LLMHandler
    from claw_agent import ClawAgent
    from curriculum import design_curriculum
    from trainer import TrainingSession

    api_key, base_url, model, recipient = _env_setup()
    if not api_key:
        sys.exit("[FAIL] LLM_API_KEY not set in .env")
    if not recipient:
        sys.exit("[FAIL] CLAW_RECIPIENT not set in .env")

    print(f"\n=== Phase 4: Single-Task Training Round ===")

    test_intent = "A rigorous and efficient programming assistant"
    print(f"Generating a minimal curriculum for: \"{test_intent}\"")

    llm = LLMHandler(api_key=api_key, base_url=base_url, model=model)
    agent = ClawAgent(recipient=recipient)

    await llm.start()
    try:
        curriculum = await design_curriculum(llm, test_intent)

        # Only run the first task of the first stage
        first_stage = curriculum.stages[0]
        first_stage.tasks = first_stage.tasks[:1]
        curriculum.stages = [first_stage]

        print(f"Running stage: [{first_stage.id}] {first_stage.name}")
        print(f"Running task : {first_stage.tasks[0].task_id}")

        session = TrainingSession(llm=llm, agent=agent, curriculum=curriculum)
        reports = await session.run()

        report = reports[0]
        tr = report.task_results[0]
        print(f"\nTask {tr.task_id} — Score: {tr.score}/10 — "
              f"{'PASSED' if tr.passed else 'FAILED'}")
        print(f"[PASS] Single-task training round completed.\n")
    finally:
        await llm.stop()


# ── Main ─────────────────────────────────────────────────────────────────────

PHASES = {
    "1": ("LLM Connection", phase1_llm_connection),
    "2": ("Curriculum Generation", phase2_curriculum),
    "3": ("Claw Agent Communication", phase3_claw_agent),
    "4": ("Single-Task Training", phase4_single_task),
}


async def run_all():
    for num, (name, fn) in PHASES.items():
        print(f"\n{'#'*60}")
        print(f"  Running Phase {num}: {name}")
        print(f"{'#'*60}")
        await fn()


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in (*PHASES, "all"):
        print(__doc__)
        sys.exit(1)

    target = sys.argv[1]
    if target == "all":
        asyncio.run(run_all())
    else:
        _, fn = PHASES[target]
        asyncio.run(fn())


if __name__ == "__main__":
    main()
