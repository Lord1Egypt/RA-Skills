"""Unit tests for AgentRuntime chat notification callbacks."""
import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import shutil

from agentpathfinder.agent_runtime import AgentRuntime
from agentpathfinder.task_engine import TaskEngine
from agentpathfinder.issuing_layer import IssuingLayer


class TestChatCallbacks(unittest.TestCase):
    """Test that notification callbacks fire correctly on state transitions."""

    def setUp(self):
        """Create temporary data directory and engine."""
        self.tmpdir = Path(tempfile.mkdtemp())
        self.engine = TaskEngine(self.tmpdir)
        self.issuing = IssuingLayer(self.engine)

        # Create a simple 2-step task
        self.task_id = self.engine.create_task(
            "test_task",
            [{"name": "step_one"}, {"name": "step_two"}]
        )

    def tearDown(self):
        """Clean up temp directory."""
        shutil.rmtree(self.tmpdir)

    def test_step_complete_callback_fires(self):
        """on_step_complete fires with correct args when step succeeds."""
        on_complete = Mock()
        on_fail = Mock()

        runtime = AgentRuntime(
            self.engine, self.issuing,
            on_step_complete=on_complete,
            on_step_fail=on_fail
        )

        def success_func():
            return "done"

        result = runtime.execute_step(self.task_id, 1, success_func)

        self.assertEqual(result["status"], "complete")
        on_complete.assert_called_once_with(1, "done")
        on_fail.assert_not_called()

    def test_step_fail_callback_fires(self):
        """on_step_fail fires with correct args when step raises exception."""
        on_complete = Mock()
        on_fail = Mock()

        runtime = AgentRuntime(
            self.engine, self.issuing,
            on_step_complete=on_complete,
            on_step_fail=on_fail
        )

        def fail_func():
            raise RuntimeError("test failure")

        result = runtime.execute_step(self.task_id, 1, fail_func)

        self.assertEqual(result["status"], "failed")
        self.assertIn("test failure", result["error"])
        on_fail.assert_called_once()
        # Check args: step_number=1, error string contains "test failure"
        args = on_fail.call_args[0]
        self.assertEqual(args[0], 1)
        self.assertIn("test failure", args[1])
        on_complete.assert_not_called()

    def test_task_complete_callback_fires(self):
        """on_task_complete fires when all steps finish successfully."""
        on_task_done = Mock()

        runtime = AgentRuntime(
            self.engine, self.issuing,
            on_task_complete=on_task_done
        )

        step_functions = {
            "step_one": lambda: "result1",
            "step_two": lambda: "result2",
        }

        result = runtime.execute_task(self.task_id, step_functions)

        on_task_done.assert_called_once()
        args = on_task_done.call_args[0]
        self.assertEqual(args[0], self.task_id)  # task_id
        self.assertEqual(args[1]["progress"], "2/2")  # formatted progress string
        self.assertTrue(args[1]["all_complete"])

    def test_callbacks_optional(self):
        """Runtime works normally when no callbacks provided."""
        runtime = AgentRuntime(self.engine, self.issuing)

        def success_func():
            return "done"

        # Should not raise
        result = runtime.execute_step(self.task_id, 1, success_func)
        self.assertEqual(result["status"], "complete")

    def test_all_three_callbacks(self):
        """All three callback types fire in a real execution flow."""
        on_complete = Mock()
        on_fail = Mock()
        on_task_done = Mock()

        runtime = AgentRuntime(
            self.engine, self.issuing,
            on_step_complete=on_complete,
            on_step_fail=on_fail,
            on_task_complete=on_task_done
        )

        step_functions = {
            "step_one": lambda: "result1",
            "step_two": lambda: "result2",
        }

        runtime.execute_task(self.task_id, step_functions)

        on_complete.assert_called()  # called twice (2 steps)
        self.assertEqual(on_complete.call_count, 2)
        on_fail.assert_not_called()
        on_task_done.assert_called_once()


if __name__ == "__main__":
    unittest.main()
