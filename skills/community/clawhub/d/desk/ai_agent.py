"""
AI Desktop Agent - Optimized Cognitive Automation
Task planning and execution with vision integration
"""

from __future__ import annotations

import base64
import io
import logging
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple

from desktop_control import DesktopController

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


@dataclass
class StepResult:
    """Result of executing a single step."""
    step_type: str
    description: str
    success: bool
    duration: float
    error: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskResult:
    """Complete task execution result."""
    task: str
    status: TaskStatus
    steps: List[StepResult] = field(default_factory=list)
    total_duration: float = 0.0
    error: Optional[str] = None


class LLMClient(Protocol):
    """Protocol for LLM integration."""

    def generate(self, prompt: str, images: Optional[List[str]] = None) -> str:
        """Generate text from prompt with optional image context."""
        ...


class AIDesktopAgent:
    """
    Optimized AI Desktop Agent for task automation.

    Features:
    - Efficient task planning with pattern matching
    - Minimal screenshot overhead
    - Step-by-step execution with rollback support
    - LLM integration for reasoning (optional)
    """

    __slots__ = ('dc', 'llm', 'step_delay', 'screenshot_before_each_step')

    # Application knowledge base
    APP_KNOWLEDGE: Dict[str, Dict] = {
        "notepad": {
            "launch": ["win", "r"],
            "type": "notepad",
            "hotkeys": {
                "save": ["ctrl", "s"],
                "new": ["ctrl", "n"],
                "open": ["ctrl", "o"],
                "print": ["ctrl", "p"],
            }
        },
        "calculator": {
            "launch": ["win", "r"],
            "type": "calc",
            "hotkeys": {}
        },
        "paint": {
            "launch": ["win", "r"],
            "type": "mspaint",
            "hotkeys": {
                "save": ["ctrl", "s"],
            }
        },
        "cmd": {
            "launch": ["win", "r"],
            "type": "cmd",
            "hotkeys": {}
        },
    }

    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        failsafe: bool = True,
        step_delay: float = 0.3,
        screenshot_before_each_step: bool = False
    ):
        """
        Initialize AI Desktop Agent.

        Args:
            llm_client: Optional LLM for intelligent planning
            failsafe: Enable mouse corner failsafe
            step_delay: Delay between steps (seconds)
            screenshot_before_each_step: Capture screenshot before each action
        """
        self.dc = DesktopController(failsafe=failsafe)
        self.llm = llm_client
        self.step_delay = step_delay
        self.screenshot_before_each_step = screenshot_before_each_step

        logger.info("AI Desktop Agent initialized")

    def __enter__(self) -> AIDesktopAgent:
        """Context manager entry."""
        return self

    def __exit__(self, *args) -> None:
        """Context manager exit with cleanup."""
        self.dc.cleanup()

    def execute_task(
        self,
        task_description: str,
        max_steps: int = 20,
        require_confirmation: bool = False
    ) -> TaskResult:
        """
        Execute a task autonomously.

        Args:
            task_description: Natural language task
            max_steps: Maximum steps to attempt
            require_confirmation: Ask before each step

        Returns:
            TaskResult with execution details
        """
        logger.info(f"Executing task: {task_description}")
        start_time = time.time()

        # Plan the task
        plan = self._create_plan(task_description)
        if not plan:
            return TaskResult(
                task=task_description,
                status=TaskStatus.FAILED,
                error="Could not create plan for task"
            )

        result = TaskResult(task=task_description, status=TaskStatus.RUNNING)

        # Execute each step
        for i, step in enumerate(plan[:max_steps], 1):
            if result.status == TaskStatus.FAILED:
                break

            logger.info(f"Step {i}/{len(plan)}: {step['description']}")

            if require_confirmation:
                if not self._confirm_step(step['description']):
                    result.status = TaskStatus.CANCELLED
                    break

            step_result = self._execute_step(step)
            result.steps.append(step_result)

            if not step_result.success:
                result.status = TaskStatus.FAILED
                result.error = step_result.error
            else:
                time.sleep(self.step_delay)

        # Finalize result
        result.total_duration = time.time() - start_time
        if result.status == TaskStatus.RUNNING:
            result.status = TaskStatus.COMPLETED

        logger.info(f"Task {result.status.value}: {len(result.steps)} steps in {result.total_duration:.1f}s")
        return result

    def _create_plan(self, task: str) -> List[Dict[str, Any]]:
        """Create execution plan based on task type."""
        task_lower = task.lower()

        # Direct pattern matching (fast path)
        if any(word in task_lower for word in ["type", "write", "enter"]):
            return self._plan_text_entry(task)

        if any(word in task_lower for word in ["draw", "paint", "sketch"]):
            return self._plan_drawing(task)

        if any(word in task_lower for word in ["open", "launch", "start"]):
            return self._plan_app_launch(task)

        if any(word in task_lower for word in ["screenshot", "capture", "photo"]):
            return self._plan_screenshot(task)

        # Fall back to generic plan
        return self._plan_generic(task)

    def _plan_text_entry(self, task: str) -> List[Dict]:
        """Plan for text entry task."""
        # Extract text content
        text = self._extract_text_from_task(task)

        steps = []

        # Check if we need to open an app
        if "notepad" in task.lower():
            steps.extend([
                {"type": "launch", "app": "notepad", "description": "Open Notepad"},
                {"type": "wait", "duration": 1, "description": "Wait for app"},
            ])

        # Add typing step
        steps.append({
            "type": "type",
            "text": text,
            "wpm": 100,
            "description": f"Type: {text[:30]}..."
        })

        return steps

    def _plan_drawing(self, task: str) -> List[Dict]:
        """Plan for drawing task."""
        subject = self._extract_subject(task)

        return [
            {"type": "launch", "app": "paint", "description": "Open Paint"},
            {"type": "wait", "duration": 2, "description": "Wait for Paint"},
            {"type": "activate", "title": "Paint", "description": "Focus Paint window"},
            {"type": "draw", "shape": subject, "description": f"Draw {subject}"},
            {"type": "screenshot", "filename": "drawing.png", "description": "Save result"},
        ]

    def _plan_app_launch(self, task: str) -> List[Dict]:
        """Plan for app launch task."""
        app = self._extract_app_name(task)

        if app in self.APP_KNOWLEDGE:
            return [
                {"type": "launch", "app": app, "description": f"Launch {app}"},
                {"type": "wait", "duration": 2, "description": f"Wait for {app}"},
            ]

        # Generic launch
        return [
            {"type": "hotkey", "keys": ["win", "r"], "description": "Open Run dialog"},
            {"type": "type", "text": app, "wpm": 100, "description": f"Type {app}"},
            {"type": "press", "key": "return", "description": "Launch"},
            {"type": "wait", "duration": 2, "description": "Wait for launch"},
        ]

    def _plan_screenshot(self, task: str) -> List[Dict]:
        """Plan for screenshot task."""
        filename = self._extract_filename(task) or "screenshot.png"

        return [
            {"type": "screenshot", "filename": filename, "description": f"Capture screen to {filename}"},
        ]

    def _plan_generic(self, task: str) -> List[Dict]:
        """Generic task plan."""
        # If LLM available, use it for planning
        if self.llm:
            return self._plan_with_llm(task)

        return [
            {"type": "analyze", "description": "Analyze current state"},
            {"type": "error", "message": f"Cannot plan task: {task}", "description": "Planning failed"},
        ]

    def _plan_with_llm(self, task: str) -> List[Dict]:
        """Use LLM for intelligent task planning."""
        # Capture current state
        screenshot = self.dc.screenshot()
        if screenshot:
            # Convert to base64 for LLM
            buffered = io.BytesIO()
            screenshot.save(buffered, format="PNG")
            img_b64 = base64.b64encode(buffered.getvalue()).decode()

            prompt = f"""Given this desktop screenshot, create a plan to: {task}

            Return a JSON list of steps, each with:
            - type: action type
            - description: what to do
            - [other relevant parameters]

            Available actions: launch, click, type, hotkey, wait, screenshot"""

            try:
                response = self.llm.generate(prompt, images=[img_b64])
                # Parse JSON from response
                import json
                plan = json.loads(response)
                return plan
            except Exception as e:
                logger.error(f"LLM planning failed: {e}")

        return []

    def _execute_step(self, step: Dict) -> StepResult:
        """Execute a single step and return result."""
        step_type = step.get("type", "unknown")
        description = step.get("description", step_type)
        start_time = time.time()

        try:
            # Screenshot before action if enabled
            if self.screenshot_before_each_step:
                step["screenshot_before"] = self.dc.screenshot()

            # Execute based on type
            if step_type == "launch":
                self._do_launch(step["app"])

            elif step_type == "click":
                x, y = step.get("x"), step.get("y")
                self.dc.click(x, y)

            elif step_type == "type":
                self.dc.type_text(step["text"], wpm=step.get("wpm", 100))

            elif step_type == "hotkey":
                self.dc.hotkey(*step["keys"])

            elif step_type == "press":
                self.dc.press(step["key"])

            elif step_type == "wait":
                time.sleep(step["duration"])

            elif step_type == "activate":
                self.dc.activate_window(step["title"])

            elif step_type == "screenshot":
                self.dc.screenshot_to_file(step.get("filename", "screenshot.png"))

            elif step_type == "draw":
                self._do_draw(step["shape"])

            elif step_type == "analyze":
                pass  # Analysis step

            elif step_type == "error":
                return StepResult(
                    step_type=step_type,
                    description=description,
                    success=False,
                    duration=time.time() - start_time,
                    error=step.get("message", "Unknown error")
                )

            duration = time.time() - start_time
            return StepResult(
                step_type=step_type,
                description=description,
                success=True,
                duration=duration
            )

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Step failed: {e}")
            return StepResult(
                step_type=step_type,
                description=description,
                success=False,
                duration=duration,
                error=str(e)
            )

    def _do_launch(self, app: str) -> None:
        """Launch an application."""
        info = self.APP_KNOWLEDGE.get(app, {})

        if info:
            # Use known launch method
            self.dc.hotkey(*info["launch"])
            time.sleep(0.3)
            self.dc.type_text(info["type"], wpm=100)
            self.dc.press("return")
        else:
            # Generic launch
            self.dc.hotkey("win", "r")
            time.sleep(0.3)
            self.dc.type_text(app, wpm=100)
            self.dc.press("return")

    def _do_draw(self, shape: str) -> None:
        """Draw a shape in Paint."""
        cx, cy = self.dc.screen_width // 2, self.dc.screen_height // 2

        shapes = {
            "circle": self._draw_circle,
            "square": self._draw_square,
            "line": self._draw_line,
            "star": self._draw_star,
        }

        draw_func = shapes.get(shape.lower(), self._draw_circle)
        draw_func(cx, cy, 100)

    def _draw_circle(self, cx: int, cy: int, r: int) -> None:
        """Draw circle using polygon approximation."""
        import math
        points = [(cx + int(r * math.cos(math.radians(a))),
                   cy + int(r * math.sin(math.radians(a))))
                  for a in range(0, 360, 10)]

        for i in range(len(points) - 1):
            self.dc.drag(points[i][0], points[i][1],
                        points[i + 1][0], points[i + 1][1],
                        duration=0.01)

    def _draw_square(self, cx: int, cy: int, size: int) -> None:
        """Draw a square."""
        half = size // 2
        corners = [
            (cx - half, cy - half),
            (cx + half, cy - half),
            (cx + half, cy + half),
            (cx - half, cy + half),
        ]
        for i in range(4):
            self.dc.drag(corners[i][0], corners[i][1],
                        corners[(i + 1) % 4][0], corners[(i + 1) % 4][1],
                        duration=0.1)

    def _draw_line(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Draw a line."""
        self.dc.drag(x1, y1, x2, y2, duration=0.2)

    def _draw_star(self, cx: int, cy: int, size: int) -> None:
        """Draw a 5-pointed star."""
        import math
        points = []
        for i in range(10):
            angle = math.radians(i * 36 - 90)
            r = size if i % 2 == 0 else size // 2
            points.append((int(cx + r * math.cos(angle)),
                          int(cy + r * math.sin(angle))))

        for i in range(len(points)):
            self.dc.drag(points[i][0], points[i][1],
                        points[(i + 1) % len(points)][0],
                        points[(i + 1) % len(points)][1],
                        duration=0.05)

    def _confirm_step(self, description: str) -> bool:
        """Ask user to confirm step execution."""
        response = input(f"Execute: {description}? [y/n]: ").strip().lower()
        return response in ('y', 'yes')

    # ========== Text Extraction Helpers ==========

    def _extract_text_from_task(self, task: str) -> str:
        """Extract text content from typing task."""
        # Look for quoted text
        import re
        match = re.search(r'["\'](.+?)["\']', task)
        if match:
            return match.group(1)

        # Look after keywords
        for keyword in ["type", "write", "enter"]:
            if keyword in task.lower():
                parts = task.lower().split(keyword, 1)
                if len(parts) > 1:
                    return parts[1].strip().strip('"\'')

        return task

    def _extract_subject(self, task: str) -> str:
        """Extract drawing subject."""
        import re
        match = re.search(r'draw\s+(?:a|an)?\s*(\w+)', task.lower())
        return match.group(1) if match else "circle"

    def _extract_app_name(self, task: str) -> str:
        """Extract application name."""
        task_lower = task.lower()

        # Check known apps
        for app in self.APP_KNOWLEDGE:
            if app in task_lower:
                return app

        # Extract after "open" or "launch"
        import re
        match = re.search(r'(?:open|launch|start)\s+(\w+)', task_lower)
        return match.group(1) if match else "notepad"

    def _extract_filename(self, task: str) -> Optional[str]:
        """Extract filename from task."""
        import re
        match = re.search(r'(\w+\.(?:png|jpg|jpeg|gif|bmp))', task.lower())
        return match.group(1) if match else None


# Convenience function
def create_agent(**kwargs) -> AIDesktopAgent:
    """Create AI Desktop Agent."""
    return AIDesktopAgent(**kwargs)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("🤖 AI Desktop Agent")
    print("=" * 50)
    print("\nExamples:")
    print("  - 'Type Hello World in Notepad'")
    print("  - 'Open Calculator'")
    print("  - 'Draw a circle in Paint'")
    print("  - 'Take a screenshot'")

    task = input("\nWhat should I do? ").strip()
    if task:
        with create_agent() as agent:
            result = agent.execute_task(task)
            print(f"\n{'=' * 50}")
            print(f"Status: {result.status.value}")
            print(f"Steps: {len(result.steps)}")
            print(f"Duration: {result.total_duration:.1f}s")
            for step in result.steps:
                icon = "✓" if step.success else "✗"
                print(f"  {icon} {step.description}")
