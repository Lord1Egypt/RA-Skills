"""Training curriculum data model and LLM-based generation.

Defines the structured curriculum format (stages, tasks, evaluation criteria)
and provides an async function to generate a curriculum from user intent via LLM.
"""

from dataclasses import dataclass, field

from loguru import logger

import config
from llm_handler import LLMHandler, Conversation

CURRICULUM_DESIGN_PROMPT = """\
You are ClawSergeant, an expert training curriculum designer for autonomous AI agents.

Your task is to design a comprehensive, multi-stage training curriculum based on \
the user's requirements. The curriculum will be used to train an AI agent (called \
"Claw") through iterative dialogue sessions.

Output a JSON object with this exact structure:
{{
  "title": "Curriculum title",
  "overview": "Brief description of the training goals",
  "target_persona": "Description of the ideal agent after training",
  "stages": [
    {{
      "id": 1,
      "name": "Stage name",
      "description": "What this stage covers",
      "objectives": ["objective 1", "objective 2"],
      "training_tasks": [
        {{
          "task_id": "1.1",
          "description": "Detailed task description",
          "scenario": "The scenario or prompt to present to the agent",
          "expected_behavior": "What a well-trained agent should do"
        }}
      ],
      "evaluation_criteria": [
        {{
          "criterion": "What is being evaluated",
          "passing_standard": "How to determine if the agent passes"
        }}
      ]
    }}
  ]
}}

Design {stage_min}-{stage_max} stages that progressively build the agent's \
capabilities. Each stage should have {tasks_min}-{tasks_max} training tasks. \
Make the training practical, specific, and challenging.
"""


@dataclass
class TrainingTask:
    """A single training task within a curriculum stage."""

    task_id: str
    description: str
    scenario: str
    expected_behavior: str


@dataclass
class EvaluationCriterion:
    """A criterion used to evaluate agent performance in a stage."""

    criterion: str
    passing_standard: str


@dataclass
class TrainingStage:
    """A single stage of the training curriculum."""

    id: int
    name: str
    description: str
    objectives: list[str]
    tasks: list[TrainingTask]
    evaluation_criteria: list[EvaluationCriterion]
    completed: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "TrainingStage":
        tasks = [
            TrainingTask(
                task_id=t["task_id"],
                description=t["description"],
                scenario=t["scenario"],
                expected_behavior=t["expected_behavior"],
            )
            for t in data.get("training_tasks", [])
        ]
        criteria = [
            EvaluationCriterion(
                criterion=c["criterion"],
                passing_standard=c["passing_standard"],
            )
            for c in data.get("evaluation_criteria", [])
        ]
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            objectives=data.get("objectives", []),
            tasks=tasks,
            evaluation_criteria=criteria,
        )


@dataclass
class Curriculum:
    """Complete training curriculum with progress tracking."""

    title: str
    overview: str
    target_persona: str
    stages: list[TrainingStage]

    @classmethod
    def from_dict(cls, data: dict) -> "Curriculum":
        stages = [TrainingStage.from_dict(s) for s in data.get("stages", [])]
        return cls(
            title=data["title"],
            overview=data["overview"],
            target_persona=data.get("target_persona", ""),
            stages=stages,
        )

    @property
    def current_stage(self) -> TrainingStage | None:
        """Return the first incomplete stage, or None if all are done."""
        for stage in self.stages:
            if not stage.completed:
                return stage
        return None

    @property
    def progress(self) -> tuple[int, int]:
        """Return (completed_count, total_count)."""
        completed = sum(1 for s in self.stages if s.completed)
        return completed, len(self.stages)

    @property
    def is_complete(self) -> bool:
        return all(s.completed for s in self.stages)


async def design_curriculum(llm: LLMHandler, user_intent: str) -> Curriculum:
    """Use the LLM to generate a training curriculum from a user intent string."""
    prompt = CURRICULUM_DESIGN_PROMPT.format(
        stage_min=config.STAGE_COUNT_MIN,
        stage_max=config.STAGE_COUNT_MAX,
        tasks_min=config.TASKS_PER_STAGE_MIN,
        tasks_max=config.TASKS_PER_STAGE_MAX,
    )
    conv = Conversation(system_prompt=prompt)
    conv.add(
        "user",
        f"Please design a training curriculum for the following requirement:\n\n"
        f"{user_intent}",
    )

    logger.info("Generating training curriculum...")
    data = await llm.chat_json(conv, temperature=config.CURRICULUM_TEMPERATURE)
    return Curriculum.from_dict(data)
