---
name: claw-sergeant
description: Train autonomous OpenClaw AI agents through LLM-guided curriculum design and multi-turn dialogue evaluation. Use this skill whenever the user wants to train, improve, or evaluate an OpenClaw agent's capabilities, design a training curriculum for an AI agent, run a training session with iterative feedback loops, or test an agent's readiness across specific skill areas. Also use when the user mentions "ClawSergeant", "agent training", "openclaw training", or wants to strengthen an AI agent's performance in areas like programming, writing, analysis, or communication.
---

# ClawSergeant: Boosting OpenClaw Agents from AI Feedback

ClawSergeant trains OpenClaw agents through a structured, LLM-driven pipeline. A Trainer LLM designs curriculum, generates training tasks, and adapts its teaching dynamically based on the agent's responses. A separate Evaluator LLM objectively scores each response, creating a feedback loop that drives iterative improvement.

## Architecture Overview

```
User Intent ──────────────────────→ LLM (Curriculum Designer)
                                          ↓
                                   Curriculum JSON (stages, tasks, criteria)
                                          ↓
Training Session Loop:
    Trainer LLM → crafts message → openclaw CLI → Claw Agent → reply
                                                      ↓
                                          Evaluator LLM → score + feedback
                                                      ↓
                              record to .claw_sergeant_accumulated_lessons/ ←──┘
                                          ↓
                                  (if failed) → Trainer LLM retries with feedback
                                          ↓
                                  (if stage passed) → stage summary for memory consolidation
                                          ↓
                    [Curriculum Pattern] → record to .claw_sergeant_accumulated_lessons/
```

## Training Pipeline

### Phase 1: Curriculum Design

The user's training intent is passed directly as input. The LLM generates a multi-stage curriculum as structured JSON based on this intent. The user reviews and approves the curriculum before training begins.

Each curriculum contains:

- **Title and overview** of the training program
- **Target persona** describing the ideal agent after training
- **3–5 stages**, each with:
  - Name, description, and learning objectives
  - 2–4 training tasks with scenario descriptions and expected behaviors
  - Evaluation criteria with passing standards

### Phase 2: Training Execution

For each stage and task, the system runs a dialogue loop:

1. **Trainer LLM** generates a task message tailored to the agent (it never sees hardcoded prompts — everything is dynamically composed)
2. Message is sent to the **Claw Agent** via `openclaw agent` CLI
3. Agent's reply is captured and fed back to the Trainer's conversation context
4. **Evaluator LLM** scores the reply (1–10) and reports strengths, weaknesses, and improvement suggestions
5. If the task is not passed and retries remain, the Trainer generates a follow-up message incorporating the evaluation feedback
6. After a stage passes, the agent receives a summary prompt to internalize lessons learned

## Environment Setup

Create a `.env` file in the project root with:

```
LLM_API_KEY=<your-api-key>          # Required: API key for the LLM
LLM_BASE_URL=https://api.openai.com/v1  # Optional: OpenAI-compatible endpoint
LLM_MODEL=gpt-4o                    # Optional: model identifier
CLAW_RECIPIENT=+15555550123         # Required: target agent's address
```

## Running the Training

### Full Training Session

```bash
python main.py "An efficient, rigorous programming assistant"
```

The training intent is passed as a command-line argument. ClawSergeant designs a curriculum, presents it for approval, and runs the training session automatically. Results are saved to `training_results.json`.

### Phase-by-Phase Testing

Use `test_phases.py` to verify each component independently before running a full session:

```bash
python test_phases.py 1    # Verify LLM API connectivity
python test_phases.py 2    # Test curriculum generation
python test_phases.py 3    # Test Claw agent communication
python test_phases.py 4    # Run a single-task training round
python test_phases.py all  # Run all phases sequentially
```

Always start with phase 1 to confirm the LLM connection works, then progress through subsequent phases.

## Configuration

All training parameters are centralized in `config.py`:

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `STAGE_COUNT_MIN` / `MAX` | 3 / 5 | Number of training stages |
| `TASKS_PER_STAGE_MIN` / `MAX` | 2 / 4 | Tasks per stage |
| `CURRICULUM_TEMPERATURE` | 0.4 | LLM temperature for curriculum design |
| `TRAINER_TEMPERATURE` | 0.7 | LLM temperature for training messages |
| `EVALUATOR_TEMPERATURE` | 0.2 | LLM temperature for evaluation (low = strict) |
| `MAX_ATTEMPTS_PER_TASK` | 2 | Retries per task before moving on |
| `STAGE_PASS_THRESHOLD` | 0.6 | Fraction of tasks needed to pass a stage |

Adjust `STAGE_PASS_THRESHOLD` higher (e.g., 0.8) for stricter training, or lower temperatures for more deterministic evaluations.

## Key Components

| File | Role |
|------|------|
| `main.py` | Entry point — orchestrates curriculum design → approval → training execution |
| `trainer.py` | Training session controller — manages dialogue loop and captures per-task/stage learnings |
| `curriculum.py` | Curriculum data model and LLM-based generation |
| `claw_agent.py` | Wraps `openclaw agent` CLI for agent communication |
| `llm_handler.py` | Async LLM client with conversation history management |
| `learning_logger.py` | Structured experience logger — records training insights and writes to OpenClaw MEMORY.md |
| `config.py` | Centralized training parameters |
| `test_phases.py` | Step-by-step pipeline verification |

## Training Results

After a session completes, `training_results.json` contains:

```json
{
  "curriculum": {
    "title": "...",
    "overview": "...",
    "target_persona": "...",
    "stages_total": 4,
    "stages_passed": 3
  },
  "stage_reports": [
    {
      "stage_id": 1,
      "stage_name": "...",
      "passed": true,
      "overall_feedback": "...",
      "tasks": [
        {
          "task_id": "1.1",
          "passed": true,
          "score": 8,
          "strengths": ["..."],
          "weaknesses": ["..."],
          "feedback": "..."
        }
      ]
    }
  ]
}
```

## Experience Recording

Training experiences are automatically recorded throughout the session. Every task evaluation, stage result, and infrastructure error is logged to `.claw_sergeant_accumulated_lessons/` as structured markdown entries for future reference.

After the session completes, a summary is written to `~/.openclaw/workspace/MEMORY.md` containing the training timestamp, curriculum details, stage pass/fail results, and a pointer to the full logs. This allows the Claw agent to reference its training history in future sessions. If the OpenClaw workspace is not found, this step is silently skipped.

## Troubleshooting

- **LLM connection fails**: Run `python test_phases.py 1` to verify API key and endpoint. Check `LLM_BASE_URL` points to a valid OpenAI-compatible API.
- **Claw agent timeout**: The default timeout is 120 seconds. If the agent is slow to respond, check network connectivity and the `openclaw` CLI installation.
- **Curriculum has no stages**: The LLM may have returned malformed JSON. Try lowering `CURRICULUM_TEMPERATURE` or switching to a more capable model.
- **All tasks fail**: Review evaluation criteria — they may be too strict. Lower `STAGE_PASS_THRESHOLD` or increase `MAX_ATTEMPTS_PER_TASK` in `config.py`.

## Dependencies

- Python 3.11+
- `httpx` — async HTTP client for LLM API calls
- `loguru` — structured logging
- `python-dotenv` — environment variable management
- `openclaw` CLI — must be installed and accessible in PATH
