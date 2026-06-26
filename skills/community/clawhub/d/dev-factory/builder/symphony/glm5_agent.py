"""GLM-5 Agent Adapter for Symphony

Translates Symphony's agent protocol to GLM-5 HTTP API calls.
Upgrades from GLM-4 to GLM-5 for better code generation.
"""

import json
import logging
import os
import urllib.request
import urllib.error
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .state_machine import SymphonyTask

logger = logging.getLogger('builder-agent.symphony.glm5_agent')


@dataclass
class AgentResult:
    """Result from agent execution"""
    success: bool
    files_created: List[str]
    files_modified: List[str]
    commands_run: List[str]
    output: str
    error: Optional[str] = None
    metadata: Dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ToolCall:
    """Represents a tool call from GLM-5"""
    type: str  # write_file, edit_file, run_command
    path: Optional[str] = None
    content: Optional[str] = None
    command: Optional[str] = None


class GLM5AgentAdapter:
    """Execute build tasks using GLM-5 API

    GLM-5 API Integration:
    - Base URL: https://api.z.ai/api/coding/paas/v4
    - Model: glm-5 (upgrade from glm-4)
    - Format: OpenAI-compatible chat completions with tool calling

    Fallback Logic:
    - GLM-5 API error → Retry with exponential backoff (1s, 2s, 4s, 8s)
    - Persistent failure → Fall back to Claude Code CLI (existing logic)
    """

    # API Configuration
    API_BASE_URL = "https://api.z.ai/api/coding/paas/v4"
    MODEL = "glm-5"  # Upgraded from glm-4

    # Retry configuration
    MAX_RETRIES = 4
    RETRY_DELAYS = [1, 2, 4, 8]  # Exponential backoff

    def __init__(self, api_key: Optional[str] = None):
        """Initialize GLM-5 agent adapter

        Args:
            api_key: GLM API key (loaded from env if not provided)
        """
        self.api_key = api_key or os.environ.get('BUILDER_GLM_API_KEY')

        if not self.api_key:
            logger.warning("GLM API key not configured")

        # Load prompts
        self.system_prompt = self._load_system_prompt()
        self.user_prompt_template = self._load_user_prompt_template()

        logger.info("GLM-5 agent adapter initialized")

    def execute_task(self, task: SymphonyTask, workspace: Path) -> AgentResult:
        """Execute a build task using GLM-5 API

        Args:
            task: Symphony task to execute
            workspace: Workspace directory

        Returns:
            Agent execution result
        """
        if not self.api_key:
            return AgentResult(
                success=False,
                files_created=[],
                files_modified=[],
                commands_run=[],
                output="",
                error="GLM API key not configured"
            )

        logger.info("Executing task %s with GLM-5", task.task_id)

        # Generate prompt
        user_prompt = self._generate_user_prompt(task)

        # Call API with retry
        response = self._call_api_with_retry(
            self.system_prompt,
            user_prompt
        )

        if not response:
            return AgentResult(
                success=False,
                files_created=[],
                files_modified=[],
                commands_run=[],
                output="",
                error="Failed to get response from GLM-5 API"
            )

        # Parse response and apply changes
        return self._process_response(response, workspace)

    def _call_api_with_retry(self, system_prompt: str, user_prompt: str) -> Optional[Dict]:
        """Call GLM-5 API with exponential backoff retry

        Args:
            system_prompt: System prompt
            user_prompt: User prompt

        Returns:
            API response dict or None if all retries fail
        """
        payload = {
            "model": self.MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.3,
            "tools": self._get_tool_definitions(),
            "tool_choice": "auto"
        }

        for attempt, delay in enumerate(self.RETRY_DELAYS):
            try:
                response = self._call_api(payload)
                if response:
                    return response

            except urllib.error.HTTPError as e:
                logger.warning("GLM-5 API HTTP error (attempt %d/%d): %s",
                             attempt + 1, len(self.RETRY_DELAYS), e.code)

                # Don't retry on 4xx errors (client errors)
                if 400 <= e.code < 500:
                    logger.error("Client error, not retrying: %s", e.code)
                    return None

            except Exception as e:
                logger.warning("GLM-5 API error (attempt %d/%d): %s",
                             attempt + 1, len(self.RETRY_DELAYS), str(e))

            # Wait before retry (except for last attempt)
            if attempt < len(self.RETRY_DELAYS) - 1:
                import time
                time.sleep(delay)

        logger.error("GLM-5 API failed after %d retries", len(self.RETRY_DELAYS))
        return None

    def _call_api(self, payload: Dict) -> Optional[Dict]:
        """Make single API call to GLM-5

        Args:
            payload: Request payload

        Returns:
            API response dict or None on error
        """
        req = urllib.request.Request(
            f"{self.API_BASE_URL}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )

        with urllib.request.urlopen(req, timeout=300) as response:
            result = json.loads(response.read().decode())
            return result

    def _process_response(self, response: Dict, workspace: Path) -> AgentResult:
        """Process GLM-5 response and apply changes to workspace

        Args:
            response: API response
            workspace: Workspace directory

        Returns:
            Agent execution result
        """
        try:
            # Extract tool calls
            message = response.get("choices", [{}])[0].get("message", {})
            tool_calls = message.get("tool_calls", [])

            if not tool_calls:
                # No tool calls, return text response
                content = message.get("content", "")
                return AgentResult(
                    success=False,
                    files_created=[],
                    files_modified=[],
                    commands_run=[],
                    output=content,
                    error="No tool calls in response"
                )

            # Process tool calls
            files_created = []
            files_modified = []
            commands_run = []
            output = []

            for tool_call in tool_calls:
                tool_type = tool_call.get("type", "")

                if tool_type == "write_file":
                    path = tool_call.get("path")
                    content = tool_call.get("content", "")

                    if path and content:
                        self._write_file(workspace, path, content)
                        files_created.append(path)
                        logger.info("Created file: %s", path)

                elif tool_type == "edit_file":
                    path = tool_call.get("path")
                    content = tool_call.get("content", "")

                    if path and content:
                        self._write_file(workspace, path, content)
                        files_modified.append(path)
                        logger.info("Modified file: %s", path)

                elif tool_type == "run_command":
                    command = tool_call.get("command")

                    if command:
                        result = self._run_command(workspace, command)
                        commands_run.append(command)
                        output.append(result)

            # Get final text content
            final_message = message.get("content", "")
            if final_message:
                output.append(final_message)

            return AgentResult(
                success=len(files_created) > 0 or len(files_modified) > 0,
                files_created=files_created,
                files_modified=files_modified,
                commands_run=commands_run,
                output="\n".join(output),
            )

        except Exception as e:
            logger.error("Failed to process GLM-5 response: %s", e)
            return AgentResult(
                success=False,
                files_created=[],
                files_modified=[],
                commands_run=[],
                output="",
                error=str(e)
            )

    def _write_file(self, workspace: Path, path: str, content: str):
        """Write a file to the workspace

        Args:
            workspace: Workspace directory
            path: File path (relative to workspace)
            content: File content
        """
        file_path = workspace / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)

    def _run_command(self, workspace: Path, command: str) -> str:
        """Run a command in the workspace

        Args:
            workspace: Workspace directory
            command: Command to run

        Returns:
            Command output
        """
        import subprocess

        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=str(workspace),
                capture_output=True,
                text=True,
                timeout=120
            )

            output = result.stdout if result.stdout else result.stderr
            return output

        except subprocess.TimeoutExpired:
            return f"Command timed out: {command}"
        except Exception as e:
            return f"Command error: {str(e)}"

    def _generate_user_prompt(self, task: SymphonyTask) -> str:
        """Generate user prompt for a task

        Args:
            task: Symphony task

        Returns:
            User prompt string
        """
        prompt = self.user_prompt_template

        # Replace placeholders
        replacements = {
            "{title}": task.title,
            "{description}": task.description,
            "{complexity}": task.complexity,
            "{url}": task.metadata.get('url', 'N/A'),
            "{source}": task.metadata.get('source', 'manual'),
        }

        for placeholder, value in replacements.items():
            prompt = prompt.replace(placeholder, value)

        return prompt

    def _load_system_prompt(self) -> str:
        """Load system prompt from file"""
        prompt_path = Path(__file__).parent / "prompts" / "system.txt"

        if prompt_path.exists():
            return prompt_path.read_text()

        # Default system prompt
        return """You are an expert software developer specializing in Python projects.

You work in an isolated workspace directory to build complete, production-ready projects.

Capabilities:
- Create complete project structures with proper packaging
- Write production-ready code with comprehensive error handling
- Generate extensive unit tests using pytest framework
- Ensure 80%+ test coverage
- Follow PEP 8 and best practices
- Add comprehensive documentation

Always think step by step before implementing:
1. Analyze the requirements
2. Design the project structure
3. Implement core functionality
4. Add comprehensive tests
5. Document the code

Use the available tools to create files and run commands as needed."""

    def _load_user_prompt_template(self) -> str:
        """Load user prompt template from file"""
        template_path = Path(__file__).parent / "prompts" / "user_template.txt"

        if template_path.exists():
            return template_path.read_text()

        # Default user prompt template
        return """Develop the following project:

Title: {title}
Description: {description}
Complexity: {complexity}
Source: {source}

Requirements:
1. Create all necessary files in the current directory
2. Include comprehensive error handling
3. Add unit tests in a tests/ directory
4. Ensure code is production-ready and well-documented
5. After creating files, run tests to verify everything works

Project Structure:
- src/ or main source files
- tests/ with comprehensive unit tests
- README.md with documentation
- requirements.txt or setup.py for dependencies

Please implement this project completely, following best practices and ensuring high test coverage."""

    def _get_tool_definitions(self) -> List[Dict]:
        """Get tool definitions for GLM-5 API

        Returns:
            List of tool definitions
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Write a new file to the workspace",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "File path relative to workspace root"
                            },
                            "content": {
                                "type": "string",
                                "description": "File content"
                            }
                        },
                        "required": ["path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "edit_file",
                    "description": "Edit an existing file in the workspace",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "File path relative to workspace root"
                            },
                            "content": {
                                "type": "string",
                                "description": "New file content"
                            }
                        },
                        "required": ["path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "run_command",
                    "description": "Run a shell command in the workspace",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "Shell command to run"
                            }
                        },
                        "required": ["command"]
                    }
                }
            }
        ]


class GLM5AgentFactory:
    """Factory for creating GLM-5 agents"""

    @staticmethod
    def create_default() -> GLM5AgentAdapter:
        """Create GLM-5 agent with default configuration"""
        return GLM5AgentAdapter()

    @staticmethod
    def create_with_api_key(api_key: str) -> GLM5AgentAdapter:
        """Create GLM-5 agent with specific API key"""
        return GLM5AgentAdapter(api_key)
