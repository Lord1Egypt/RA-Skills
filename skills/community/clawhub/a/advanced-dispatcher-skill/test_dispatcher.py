import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from dispatcher import DispatcherRouter, RoutingError


class DispatcherRouterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.router = DispatcherRouter()

    def test_code_architecture_routes_to_gpt_5_4(self) -> None:
        plan = self.router.route("design this service", domain="code-architecture")
        self.assertEqual(plan.mode, "standard")
        self.assertEqual(plan.primary.model, "openai-codex/gpt-5.4")
        self.assertEqual(plan.primary.cache_retention, "long")

    def test_math_algorithms_routes_to_glm_5(self) -> None:
        plan = self.router.route("prove runtime bound", domain="math-algorithms")
        self.assertEqual(plan.primary.model, "opencode-go/glm-5")
        self.assertEqual(plan.primary.cache_retention, "short")

    def test_web_brainstorming_routes_to_minimax(self) -> None:
        plan = self.router.route("brainstorm landing page variants", domain="web-brainstorming")
        self.assertEqual(plan.primary.model, "opencode-go/minimax-m2.5")

    def test_research_routes_to_kimi(self) -> None:
        plan = self.router.route("read these long docs", domain="research-long-context")
        self.assertEqual(plan.primary.model, "opencode-go/kimi-k2.5")

    def test_quick_scripts_routes_to_spark(self) -> None:
        plan = self.router.route("format this csv", domain="quick-scripts-formatting")
        self.assertEqual(plan.primary.model, "openai-codex/gpt-5.3-codex-spark")
        self.assertEqual(plan.primary.cache_retention, "long")

    def test_buildq_pipeline_shape(self) -> None:
        plan = self.router.route("buildq: fix CLI parser", domain="code-architecture")
        self.assertEqual(plan.mode, "buildq")
        self.assertEqual(len(plan.pipeline), 5)
        self.assertEqual(plan.pipeline[0].name, "plan")
        self.assertEqual(plan.pipeline[0].run.model, "openai-codex/gpt-5.4")
        self.assertEqual(plan.pipeline[2].run.model, "opencode-go/glm-5")
        self.assertEqual(plan.pipeline[3].run.model, "openai-codex/gpt-5.3-codex")

    def test_build_pipeline_shape_and_models(self) -> None:
        plan = self.router.route("build: implement auth service", domain="code-architecture")
        self.assertEqual(plan.mode, "build")
        self.assertEqual(len(plan.pipeline), 10)
        self.assertEqual(
            [step.name for step in plan.pipeline[:4]],
            ["parallel-plan-a", "parallel-plan-b", "judge-plan", "boilerplate"],
        )
        self.assertEqual(plan.pipeline[0].run.model, "openai-codex/gpt-5.4")
        self.assertEqual(plan.pipeline[1].run.model, "opencode-go/glm-5")
        self.assertEqual(plan.pipeline[2].run.model, "openai-codex/gpt-5.4")
        self.assertEqual(plan.pipeline[3].run.model, "openai-codex/gpt-5.3-codex-spark")
        self.assertEqual(plan.pipeline[6].run.model, "openai-codex/gpt-5.3-codex")
        self.assertEqual(plan.pipeline[-1].run.model, "opencode-go/glm-5")

    def test_buildx_pipeline_shape_and_second_reviewer(self) -> None:
        plan = self.router.route("buildx: refactor multi-module backend", domain="code-architecture")
        self.assertEqual(plan.mode, "buildx")
        self.assertEqual(len(plan.pipeline), 12)
        self.assertEqual(plan.pipeline[10].name, "review-resolve-b")
        self.assertEqual(plan.pipeline[10].run.model, "opencode-go/kimi-k2.5")
        self.assertEqual(plan.pipeline[-1].run.model, "opencode-go/glm-5")

    def test_claude_never_appears_in_build_pipelines(self) -> None:
        for prompt in (
            "buildq: fix parser",
            "build: implement auth service --force-claude",
            "buildx: refactor backend",
        ):
            with self.subTest(prompt=prompt):
                plan = self.router.route(prompt, domain="code-architecture")
                self.assertTrue(plan.pipeline)
                all_models = [step.run.model for step in plan.pipeline]
                self.assertNotIn("anthropic/claude-sonnet-4-6", all_models)
                self.assertNotIn("anthropic/claude-opus-4-6", all_models)

    def test_tradeoff_default_parallel_and_judge(self) -> None:
        plan = self.router.route(
            "evaluate tradeoffs for these architectures",
            domain="code-architecture",
        )
        self.assertEqual(plan.mode, "tradeoff")
        self.assertEqual(
            tuple(run.model for run in plan.parallel),
            ("opencode-go/glm-5", "openai-codex/gpt-5.3-codex"),
        )
        self.assertEqual(plan.judge.model, "openai-codex/gpt-5.4")
        self.assertEqual(plan.parallel[0].cache_retention, "short")
        self.assertEqual(plan.parallel[1].cache_retention, "long")
        self.assertEqual(plan.judge.cache_retention, "long")

    def test_tradeoff_force_claude_only_for_container_prompt(self) -> None:
        plan = self.router.route(
            "compare approaches for the migration --force-claude",
            domain="code-architecture",
        )
        self.assertEqual(plan.mode, "tradeoff-force-claude")
        self.assertEqual(
            tuple(run.model for run in plan.parallel),
            ("anthropic/claude-sonnet-4-6", "anthropic/claude-opus-4-6"),
        )
        self.assertEqual(plan.judge.model, "openai-codex/gpt-5.4")
        self.assertTrue(plan.used_force_claude)

    def test_force_claude_does_not_change_standard_route(self) -> None:
        plan = self.router.route(
            "build the endpoint --force-claude",
            domain="code-architecture",
        )
        self.assertEqual(plan.mode, "standard")
        self.assertEqual(plan.primary.model, "openai-codex/gpt-5.4")
        self.assertTrue(plan.used_force_claude)

    def test_legacy_flags_are_rejected(self) -> None:
        for flag in ("--use-claude", "--force-opus", "--no-opus"):
            with self.subTest(flag=flag):
                with self.assertRaises(RoutingError):
                    self.router.route(f"evaluate tradeoffs {flag}", domain="code-architecture")

    def test_empty_prompt_raises(self) -> None:
        with self.assertRaises(RoutingError):
            self.router.route("   ", domain="code-architecture")

    def test_invalid_domain_raises(self) -> None:
        with self.assertRaises(RoutingError):
            self.router.route("hello", domain="creative")

    def test_smoke_end_to_end_tradeoff_shape(self) -> None:
        prompt = "evaluate tradeoffs for event bus vs direct calls in production"
        plan = self.router.route(prompt, domain="code-architecture")
        self.assertEqual(plan.mode, "tradeoff")
        self.assertEqual(len(plan.parallel), 2)
        self.assertIsNotNone(plan.judge)
        all_models = [run.model for run in plan.parallel] + [plan.judge.model]
        self.assertNotIn("anthropic/claude-sonnet-4-6", all_models)
        self.assertNotIn("anthropic/claude-opus-4-6", all_models)

    def test_smoke_build_modes(self) -> None:
        for prompt, expected in (
            ("buildq: fix parser", "buildq"),
            ("build: implement auth service", "build"),
            ("buildx: refactor backend", "buildx"),
        ):
            with self.subTest(prompt=prompt):
                plan = self.router.route(prompt, domain="code-architecture")
                self.assertEqual(plan.mode, expected)
                self.assertTrue(plan.pipeline)


if __name__ == "__main__":
    unittest.main(verbosity=2)
