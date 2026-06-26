"""Multi-turn training session controller.

Orchestrates the dialogue loop between a trainer LLM (ClawSergeant),
a real OpenClaw agent (the trainee), and an evaluator LLM. The trainer
LLM dynamically generates every message sent to the Claw agent, adapting
its approach based on the agent's responses and evaluation results.
"""

from dataclasses import dataclass
from typing import Callable

from loguru import logger

import config
from llm_handler import LLMHandler, Conversation
from claw_agent import ClawAgent
from curriculum import Curriculum, TrainingStage, TrainingTask
from learning_logger import LearningLogger

TRAINER_SYSTEM_PROMPT = """\
You are ClawSergeant, a strict but encouraging trainer for autonomous AI agents.

You are training an AI agent (the "Claw") through direct dialogue. The agent \
receives your messages directly, so write naturally as if you were \
talking to it. Your role:
1. Present training tasks and scenarios clearly
2. Adapt your teaching style based on the agent's responses
3. Provide targeted guidance when the agent struggles
4. Progressively raise the bar as the agent improves

Current Training Context:
- Curriculum: {curriculum_title}
- Target Persona: {target_persona}
- Current Stage: [{stage_id}] {stage_name}
- Stage Description: {stage_description}
- Stage Objectives: {stage_objectives}

IMPORTANT: Output ONLY the message to send to the Claw agent. Do not include \
any meta-commentary, labels like "[Trainer]", or markdown fences. Write the \
message exactly as the agent should receive it.
"""

BRIEFING_TEMPLATE = """\
You are required to undergo "{curriculum_title}" training to strengthen your \
capabilities in the following areas:

{objectives_summary}

Target profile after training: {target_persona}

The training consists of {stage_count} stages:
{stage_list}

IMPORTANT: During the training process, you must actively summarize and \
accumulate lessons learned from each exercise. These experiences should be \
remembered for future reference and continuous self-improvement. Treat every \
task as an opportunity to refine your understanding and performance.

Confirm that you understand the training objectives and are ready to begin.\
"""

STAGE_SUMMARY_TEMPLATE = """\
You have completed Stage {stage_id}: {stage_name} ({passed}/{total} tasks passed).

Now, remember this, summarize the key lessons and experiences you gained \
from this stage. What worked well? What patterns or principles did you learn? \
Internalize these insights — they will be essential for the upcoming stages \
and your future performance.\
"""

EVALUATOR_PROMPT = """\
Evaluate the Claw agent's response to the given training task.

Task requirements: {task_description}
Expected behavior: {expected_behavior}
Evaluation criteria:
{criteria}

The Claw agent's response:
{agent_response}

Provide your evaluation as a JSON object:
{{
  "passed": true/false,
  "score": 1-10,
  "strengths": ["strength 1", "strength 2"],
  "weaknesses": ["weakness 1", "weakness 2"],
  "feedback": "Detailed feedback for the agent",
  "suggestion": "Specific suggestion for improvement"
}}
"""



@dataclass
class TaskResult:
    """Result of a single training task evaluation."""

    task_id: str
    passed: bool
    score: int
    strengths: list[str]
    weaknesses: list[str]
    feedback: str
    suggestion: str


@dataclass
class StageReport:
    """Summary report for a completed training stage."""

    stage_id: int
    stage_name: str
    passed: bool
    task_results: list[TaskResult]
    overall_feedback: str


OutputFunc = Callable[[str], None]


class TrainingSession:
    """Controls the multi-turn training flow between trainer LLM and Claw agent.

    For each task the Trainer LLM dynamically generates the message sent to the
    real Claw agent, sees the agent's reply, receives evaluation results, and
    decides how to phrase the retry — making the LLM the true driver of the
    training dialogue.
    """

    def __init__(
        self,
        llm: LLMHandler,
        agent: ClawAgent,
        curriculum: Curriculum,
        on_output: OutputFunc | None = None,
        learnings: LearningLogger | None = None,
    ):
        self._llm = llm
        self._agent = agent
        self._curriculum = curriculum
        self._out = on_output or print
        self._learnings = learnings or LearningLogger()
        self._trainer_conv = Conversation()
        self._stage_reports: list[StageReport] = []

    @property
    def curriculum(self) -> Curriculum:
        return self._curriculum

    @property
    def reports(self) -> list[StageReport]:
        return list(self._stage_reports)

    # -- briefing --------------------------------------------------------------

    def _build_briefing(self) -> str:
        """Construct the explicit training briefing sent to the agent."""
        cur = self._curriculum
        all_objectives: list[str] = []
        for stage in cur.stages:
            all_objectives.extend(stage.objectives)
        objectives_summary = "\n".join(f"- {obj}" for obj in all_objectives)

        stage_list = "\n".join(
            f"  Stage {s.id}: {s.name} ({len(s.tasks)} tasks)"
            for s in cur.stages
        )
        return BRIEFING_TEMPLATE.format(
            curriculum_title=cur.title,
            objectives_summary=objectives_summary,
            target_persona=cur.target_persona,
            stage_count=len(cur.stages),
            stage_list=stage_list,
        )

    async def _send_briefing(self) -> str:
        """Send the training briefing to the Claw agent and return its reply."""
        briefing = self._build_briefing()
        self._out(f"\n[Briefing -> Claw Agent]\n{briefing}")

        self._out("\n[Sending briefing via openclaw...]")
        try:
            reply = await self._agent.send(briefing)
        except RuntimeError as exc:
            reply = f"[Agent communication error: {exc}]"
            self._out(f"\n[ERROR] {exc}")
            self._learnings.log_error(
                error_msg=str(exc),
                context="Sending training briefing to Claw agent",
            )
        self._out(f"\n[Claw Agent]\n{reply}")
        return reply

    # -- stage summary ---------------------------------------------------------

    async def _send_stage_summary(
        self, stage: TrainingStage, passed: int, total: int
    ) -> str:
        """Prompt the agent to summarize and remember lessons from a passed stage."""
        msg = STAGE_SUMMARY_TEMPLATE.format(
            stage_id=stage.id,
            stage_name=stage.name,
            passed=passed,
            total=total,
        )
        self._out(f"\n[Summary Prompt -> Claw Agent]\n{msg}")
        self._out("\n[Sending summary prompt via openclaw...]")
        try:
            reply = await self._agent.send(msg)
        except RuntimeError as exc:
            reply = f"[Agent communication error: {exc}]"
            self._out(f"\n[ERROR] {exc}")
            self._learnings.log_error(
                error_msg=str(exc),
                context=f"Sending stage {stage.id} summary to Claw agent",
                stage_name=stage.name,
            )
        self._out(f"\n[Claw Agent Summary]\n{reply}")
        return reply

    # -- prompt builders -------------------------------------------------------

    def _build_trainer_prompt(self, stage: TrainingStage) -> str:
        return TRAINER_SYSTEM_PROMPT.format(
            curriculum_title=self._curriculum.title,
            target_persona=self._curriculum.target_persona,
            stage_id=stage.id,
            stage_name=stage.name,
            stage_description=stage.description,
            stage_objectives=", ".join(stage.objectives),
        )

    # -- evaluation ------------------------------------------------------------

    async def _evaluate_response(
        self,
        task: TrainingTask,
        agent_response: str,
        stage: TrainingStage,
    ) -> TaskResult:
        """Have the LLM objectively evaluate the Claw agent's response."""
        criteria_text = "\n".join(
            f"- {c.criterion}: {c.passing_standard}"
            for c in stage.evaluation_criteria
        )
        eval_conv = Conversation(
            system_prompt=(
                "You are an objective AI training evaluator. "
                "Always respond in valid JSON."
            )
        )
        eval_conv.add(
            "user",
            EVALUATOR_PROMPT.format(
                task_description=task.description,
                expected_behavior=task.expected_behavior,
                criteria=criteria_text,
                agent_response=agent_response,
            ),
        )

        result = await self._llm.chat_json(eval_conv, temperature=config.EVALUATOR_TEMPERATURE)
        return TaskResult(
            task_id=task.task_id,
            passed=result.get("passed", False),
            score=result.get("score", 0),
            strengths=result.get("strengths", []),
            weaknesses=result.get("weaknesses", []),
            feedback=result.get("feedback", ""),
            suggestion=result.get("suggestion", ""),
        )

    # -- trainer LLM interaction -----------------------------------------------

    async def _trainer_generate(self, instruction: str) -> str:
        """Ask the Trainer LLM to produce the next message for the Claw agent.

        *instruction* is an internal directive that the Trainer LLM sees (as a
        user-role message in its conversation) but the Claw agent never sees.
        The LLM's reply is what gets forwarded to the agent.
        """
        self._trainer_conv.add("user", instruction)
        reply = await self._llm.chat(self._trainer_conv, temperature=config.TRAINER_TEMPERATURE)
        return reply

    # -- single task -----------------------------------------------------------

    async def _run_task(
        self,
        stage: TrainingStage,
        task: TrainingTask,
    ) -> TaskResult:
        """Run a single training task with up to config.MAX_ATTEMPTS_PER_TASK tries."""
        max_attempts = config.MAX_ATTEMPTS_PER_TASK
        self._out(f"\n{'='*60}")
        self._out(f"  Task {task.task_id}: {task.description}")
        self._out(f"{'='*60}")

        result: TaskResult | None = None
        for attempt in range(1, max_attempts + 1):
            self._out(
                f"\n[Trainer LLM] Generating training prompt "
                f"(attempt {attempt}/{max_attempts})..."
            )

            # Have the Trainer LLM craft the message dynamically
            if attempt == 1:
                instruction = (
                    f"Present the following training task to the Claw agent. "
                    f"Craft a clear, well-structured message that the agent "
                    f"will receive directly.\n\n"
                    f"Task ID: {task.task_id}\n"
                    f"Description: {task.description}\n"
                    f"Scenario:\n{task.scenario}\n"
                    f"Expected behavior: {task.expected_behavior}"
                )
            else:
                instruction = (
                    f"The agent's previous response did not fully meet the "
                    f"standards. Here is the evaluation:\n\n"
                    f"Score: {result.score}/10\n"
                    f"Weaknesses: {', '.join(result.weaknesses)}\n"
                    f"Feedback: {result.feedback}\n"
                    f"Suggestion: {result.suggestion}\n\n"
                    f"Generate a follow-up message to help the agent improve. "
                    f"You may rephrase the task, provide hints, or break it "
                    f"into smaller steps — whatever you think will be most "
                    f"effective as a trainer."
                )

            trainer_msg = await self._trainer_generate(instruction)
            self._out(f"\n[Trainer LLM -> Claw Agent]\n{trainer_msg}")

            # Send the LLM-generated message to the real Claw agent
            self._out("\n[Sending to Claw Agent via openclaw...]")
            try:
                claw_response = await self._agent.send(trainer_msg)
            except RuntimeError as exc:
                self._out(f"\n[ERROR] Failed to communicate with Claw agent: {exc}")
                claw_response = f"[Agent communication error: {exc}]"
                self._learnings.log_error(
                    error_msg=str(exc),
                    context=f"Sending task {task.task_id} message to Claw agent",
                    stage_name=stage.name,
                    task_id=task.task_id,
                )

            self._out(f"\n[Claw Agent]\n{claw_response}")

            # Feed the agent's response back into the trainer conversation
            # so the LLM has full dialogue context for subsequent turns
            self._trainer_conv.add(
                "user",
                f"The Claw agent responded:\n\n{claw_response}",
            )

            # Objective evaluation via a separate LLM call
            self._out("\n[Evaluator] Assessing response...")
            result = await self._evaluate_response(task, claw_response, stage)

            status = "PASSED" if result.passed else "NEEDS IMPROVEMENT"
            self._out(f"\n[Evaluation] Score: {result.score}/10 | {status}")
            if result.strengths:
                self._out(f"  Strengths: {', '.join(result.strengths)}")
            if result.weaknesses:
                self._out(f"  Weaknesses: {', '.join(result.weaknesses)}")
            self._out(f"  Feedback: {result.feedback}")

            self._learnings.log_task_result(
                task_id=task.task_id,
                task_description=task.description,
                passed=result.passed,
                score=result.score,
                strengths=result.strengths,
                weaknesses=result.weaknesses,
                feedback=result.feedback,
                stage_name=stage.name,
                curriculum_title=self._curriculum.title,
            )

            if result.passed:
                return result

        assert result is not None
        return result

    # -- single stage ----------------------------------------------------------

    async def _run_stage(self, stage: TrainingStage) -> StageReport:
        """Run all tasks in a training stage and produce a report."""
        self._out(f"\n{'#'*60}")
        self._out(f"  Stage {stage.id}: {stage.name}")
        self._out(f"  {stage.description}")
        self._out(f"{'#'*60}")
        self._out("\nObjectives:")
        for obj in stage.objectives:
            self._out(f"  - {obj}")

        # Fresh trainer conversation per stage, carrying the stage context
        self._trainer_conv = Conversation(
            system_prompt=self._build_trainer_prompt(stage)
        )

        task_results: list[TaskResult] = []
        for task in stage.tasks:
            result = await self._run_task(stage, task)
            task_results.append(result)

        passed_count = sum(1 for r in task_results if r.passed)
        total = len(task_results)
        stage_passed = passed_count >= (total * config.STAGE_PASS_THRESHOLD)

        overall = (
            f"Stage {stage.id} '{stage.name}': "
            f"{passed_count}/{total} tasks passed. "
            f"{'Stage PASSED.' if stage_passed else 'Stage FAILED — review and retrain recommended.'}"
        )
        stage.completed = stage_passed

        report = StageReport(
            stage_id=stage.id,
            stage_name=stage.name,
            passed=stage_passed,
            task_results=task_results,
            overall_feedback=overall,
        )
        self._stage_reports.append(report)

        task_summaries = [
            f"Task {r.task_id}: {'PASSED' if r.passed else 'FAILED'} "
            f"({r.score}/10)"
            for r in task_results
        ]
        self._learnings.log_stage_result(
            stage_id=stage.id,
            stage_name=stage.name,
            passed=stage_passed,
            tasks_passed=passed_count,
            tasks_total=total,
            curriculum_title=self._curriculum.title,
            task_summaries=task_summaries,
        )

        marker = "PASSED" if stage_passed else "FAILED"
        self._out(f"\n{'='*60}")
        self._out(f"  Stage Result: {marker}")
        self._out(f"  Tasks Passed: {passed_count}/{total}")
        self._out(f"{'='*60}")

        if stage_passed:
            await self._send_stage_summary(stage, passed_count, total)

        return report

    # -- full session ----------------------------------------------------------

    async def run(self) -> list[StageReport]:
        """Execute the complete training session across all stages."""
        self._out(f"\n{'*'*60}")
        self._out("  ClawSergeant Training Session")
        self._out(f"  Curriculum: {self._curriculum.title}")
        self._out(f"  Stages: {len(self._curriculum.stages)}")
        self._out(f"{'*'*60}")

        # Send explicit training briefing before the first task
        await self._send_briefing()

        for stage in self._curriculum.stages:
            report = await self._run_stage(stage)
            if not report.passed:
                self._out(
                    f"\n[ClawSergeant] Stage {stage.id} was not passed. "
                    f"Continuing to next stage for exposure, "
                    f"but retraining is recommended."
                )

        completed, total = self._curriculum.progress
        self._out(f"\n{'*'*60}")
        self._out("  Training Complete!")
        self._out(f"  Stages Passed: {completed}/{total}")
        if self._curriculum.is_complete:
            self._out("  Status: ALL STAGES PASSED — Agent is ready!")
        else:
            self._out("  Status: PARTIAL — Some stages need retraining")
        self._out(f"{'*'*60}")

        return list(self._stage_reports)
