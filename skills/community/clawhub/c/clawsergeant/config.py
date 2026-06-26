"""Centralized training configuration for ClawSergeant.

Adjust these values to control training scale, difficulty, and behavior.
"""

# ── Curriculum Generation ────────────────────────────────────────────────────

# Number of training stages the LLM should design
STAGE_COUNT_MIN = 3
STAGE_COUNT_MAX = 5

# Number of training tasks per stage
TASKS_PER_STAGE_MIN = 2
TASKS_PER_STAGE_MAX = 4

# LLM temperature for curriculum generation (lower = more deterministic)
CURRICULUM_TEMPERATURE = 0.4

# ── Training Session ─────────────────────────────────────────────────────────

# Max attempts per task before moving on (1 = no retries)
MAX_ATTEMPTS_PER_TASK = 2

# Fraction of tasks that must pass for a stage to be considered passed
STAGE_PASS_THRESHOLD = 0.6

# ── LLM Temperatures ─────────────────────────────────────────────────────────

# Temperature for the Trainer LLM when generating messages to the agent
TRAINER_TEMPERATURE = 0.7

# Temperature for the Evaluator LLM when scoring agent responses
EVALUATOR_TEMPERATURE = 0.2
