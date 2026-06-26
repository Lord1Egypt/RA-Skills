"""ClawSergeant — Train autonomous AI agents through LLM-guided curriculum.

Entry point that orchestrates the two-phase training pipeline:
  1. Design a multi-stage curriculum via LLM based on the user's intent
  2. Run the training session with multi-turn dialogue (after user approval)
"""

import asyncio
import json
import logging
import os
import sys

from dotenv import load_dotenv
from loguru import logger

from llm_handler import LLMHandler
from claw_agent import ClawAgent
from curriculum import Curriculum, design_curriculum
from trainer import TrainingSession
from learning_logger import LearningLogger


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


def _configure_logging() -> None:
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logging.basicConfig(handlers=[_InterceptHandler()], level=0, force=True)


BANNER = """\

============================================================
  ClawSergeant: Training Autonomous AI Agents
  Powered by LLM-guided Curriculum Design
============================================================
"""


def _print_curriculum_summary(curriculum: Curriculum) -> None:
    """Display a human-readable overview of the generated curriculum."""
    print(f"\n--- Curriculum: {curriculum.title} ---")
    print(f"Overview : {curriculum.overview}")
    print(f"Target   : {curriculum.target_persona}")
    print(f"Stages   : {len(curriculum.stages)}")
    for stage in curriculum.stages:
        print(f"  [{stage.id}] {stage.name} — {len(stage.tasks)} tasks")


def _save_results(
    curriculum: Curriculum, reports: list, filename: str = "training_results.json"
) -> None:
    """Persist training results to a JSON file for later review."""
    output = {
        "curriculum": {
            "title": curriculum.title,
            "overview": curriculum.overview,
            "target_persona": curriculum.target_persona,
            "stages_total": len(curriculum.stages),
            "stages_passed": sum(1 for s in curriculum.stages if s.completed),
        },
        "stage_reports": [
            {
                "stage_id": r.stage_id,
                "stage_name": r.stage_name,
                "passed": r.passed,
                "overall_feedback": r.overall_feedback,
                "tasks": [
                    {
                        "task_id": tr.task_id,
                        "passed": tr.passed,
                        "score": tr.score,
                        "strengths": tr.strengths,
                        "weaknesses": tr.weaknesses,
                        "feedback": tr.feedback,
                    }
                    for tr in r.task_results
                ],
            }
            for r in reports
        ],
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nTraining results saved to {filename}")


async def main(user_intent: str) -> None:
    _configure_logging()
    load_dotenv()

    llm_api_key = os.getenv("LLM_API_KEY")
    if not llm_api_key:
        sys.exit(
            "Missing LLM_API_KEY. "
            "Please set it in your .env file (see .env.example)."
        )

    claw_recipient = os.getenv("CLAW_RECIPIENT", "")
    if not claw_recipient:
        sys.exit(
            "Missing CLAW_RECIPIENT. "
            "Please set the target agent's address in your .env file."
        )

    llm = LLMHandler(
        api_key=llm_api_key,
        base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1"),
        model=os.getenv("LLM_MODEL", "gpt-4o"),
    )
    agent = ClawAgent(recipient=claw_recipient)
    learnings = LearningLogger()

    print(BANNER)
    print(f"Training intent: {user_intent}\n")

    await llm.start()
    try:
        # Phase 1: design the curriculum
        print("Designing training curriculum based on your requirements...")
        curriculum = await design_curriculum(llm, user_intent)
        _print_curriculum_summary(curriculum)

        confirm = input("\nReady to start training? (y/n): ").strip().lower()
        if confirm not in ("y", "yes", ""):
            print("Training cancelled.")
            return

        # Phase 2: run the training session against the real Claw agent
        session = TrainingSession(
            llm=llm, agent=agent, curriculum=curriculum,
            learnings=learnings,
        )
        reports = await session.run()

        _save_results(curriculum, reports)

        # Record curriculum-level patterns for future reference
        completed, total_stages = curriculum.progress
        effective = [
            f"Stage {s.id} '{s.name}' passed"
            for s in curriculum.stages if s.completed
        ]
        ineffective = [
            f"Stage {s.id} '{s.name}' failed"
            for s in curriculum.stages if not s.completed
        ]
        learnings.log_curriculum_pattern(
            curriculum_title=curriculum.title,
            target_persona=curriculum.target_persona,
            stages_total=total_stages,
            stages_passed=completed,
            effective_patterns=effective,
            ineffective_patterns=ineffective,
        )

        # Print learning stats
        stats = learnings.stats()
        total_entries = sum(stats.values())
        lessons_dir = os.path.abspath(learnings._dir)
        print(f"\n[Learning Memory] Session recorded {total_entries} entries "
              f"to {lessons_dir}")

        # Write training summary to OpenClaw workspace MEMORY.md
        stage_details = [
            f"Stage {s.id} '{s.name}': "
            f"{'PASSED' if s.completed else 'FAILED'}"
            for s in curriculum.stages
        ]
        written = learnings.write_to_openclaw_memory(
            curriculum_title=curriculum.title,
            target_persona=curriculum.target_persona,
            stages_passed=completed,
            stages_total=total_stages,
            stage_details=stage_details,
            lessons_dir=lessons_dir,
        )
        if written:
            print("[Learning Memory] Training summary written to "
                  "OpenClaw workspace MEMORY.md")

    finally:
        await llm.stop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(
            "Usage: python main.py <training-intent>\n"
            "Example: python main.py 'An efficient programming assistant'"
        )
    asyncio.run(main(user_intent=" ".join(sys.argv[1:])))
