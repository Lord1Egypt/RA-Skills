---
name: dimos-robotics-dev
description: Build, review, and troubleshoot DimOS robotics applications, especially DimOS @skill methods, Module classes, Blueprints, MCP wiring, CLI runs, replay/simulation testing, and safe robot-control scaffolds.
---

# DimOS Robotics Development Skill

Use this skill when a user asks to build, modify, explain, debug, or package work for the DimensionalOS/DimOS robotics repo, including robot `@skill` methods, `Module` classes, `Blueprint`s, MCP tools, CLI workflows, Unitree Go2/G1, drones, xArm, replay data, or simulation.

## Core mental model

DimOS is an agentic operating system for robotics. Treat a DimOS application as a graph of `Module`s connected by typed streams and RPC. A `Blueprint` composes modules into a runnable stack. A DimOS `@skill` is a method on a `Module` that is exposed to agents and MCP clients as a callable tool.

When writing code, prefer the DimOS-native style:

- Put imports at the top of the file.
- Use `Module` subclasses for robot subsystems and skill containers.
- Use `In[T]` and `Out[T]` streams for dataflow.
- Use `@rpc` for non-agent RPC methods.
- Use `@skill` for agent-exposed actions; do not stack `@rpc` on the same method because `@skill` already wraps the method for RPC.
- Add a clear docstring to every `@skill`; DimOS exposes the docstring as the tool description.
- Type-annotate every public skill parameter.
- Return a descriptive `str` from skills unless the current DimOS code path explicitly supports another return type.
- Keep skill parameters simple and JSON-serializable: `str`, `int`, `float`, `bool`, and simple lists are safest.
- Do not assume a skill exists. Tell the user to verify with `dimos mcp list-tools` or inspect the relevant skill container.

## Safety-first robotics behavior

For any physical robot behavior:

1. Prefer replay or simulation before real hardware.
2. Add conservative limits around movement, speed, turn angle, distance, and duration.
3. Make unsafe requests fail closed with a clear string response rather than executing partially.
4. Do not generate code that disables emergency stops, bypasses collision checks, hides robot state, or removes safety limits.
5. For real hardware, require local supervision, a clear area, charged battery, network stability, and an accessible emergency stop.
6. Do not claim a robot action happened unless the code receives a success signal or the underlying method returns success.

## Common DimOS commands

Use these commands as the default workflow when helping a user test a DimOS skill:

```bash
# List runnable blueprints
dimos list

# Start a replay or simulation stack first
dimos --replay run unitree-go2-agentic --daemon
dimos --simulation run unitree-go2-agentic --daemon

# Inspect runtime state
dimos status
dimos log -f

# Discover and call MCP skills
dimos mcp list-tools
dimos mcp modules
dimos mcp call <tool_name> --arg key=value

# Send natural-language input to the running agent
dimos agent-send "describe what you can do"

# Stop the stack
dimos stop
```

For real robot examples, keep IPs as placeholders unless the user supplies a real one:

```bash
dimos run unitree-go2-agentic --robot-ip <ROBOT_IP>
```

## Writing a DimOS skill container

Generate skill containers in this shape:

```python
from __future__ import annotations

from dimos.agents.annotation import skill
from dimos.core.core import rpc
from dimos.core.module import Module


class ExampleSkillContainer(Module):
    @rpc
    def start(self) -> None:
        super().start()

    @rpc
    def stop(self) -> None:
        super().stop()

    @skill
    def say_status(self) -> str:
        """Report that this skill container is running."""
        return "ExampleSkillContainer is running."


example_skill_container = ExampleSkillContainer.blueprint()
```

If the skill needs another module, use the DimOS Spec pattern instead of stringly typed lookups:

```python
from typing import Protocol

from dimos.spec.utils import Spec


class NavigatorSpec(Spec, Protocol):
    def set_goal(self, x: float, y: float) -> bool: ...


class NavigationSkillContainer(Module):
    _navigator: NavigatorSpec

    @skill
    def go_to_xy(self, x: float, y: float) -> str:
        """Navigate to a map coordinate.

        Args:
            x: Target x coordinate in meters.
            y: Target y coordinate in meters.
        """
        ok = self._navigator.set_goal(x, y)
        return "Navigation goal accepted." if ok else "Navigation goal failed."
```

## Wiring a skill into an agentic blueprint

For MCP tools, include both `McpServer` and `McpClient` in the blueprint along with the robot stack and skill containers:

```python
from dimos.agents.mcp.mcp_client import McpClient
from dimos.agents.mcp.mcp_server import McpServer
from dimos.core.coordination.blueprints import autoconnect

from my_project.example_skill_container import ExampleSkillContainer


my_agentic_blueprint = autoconnect(
    # robot_stack(),
    McpServer.blueprint(),
    McpClient.blueprint(),
    ExampleSkillContainer.blueprint(),
)
```

Expose a module-level blueprint variable so `dimos run <blueprint>` can find it. If adding or renaming blueprints inside the DimOS repo, run the registry-generation test that updates `dimos/robot/all_blueprints.py`.

## Review checklist for generated code

Before giving final code, check:

- Each `@skill` has a docstring and typed parameters.
- Skill methods return a useful string.
- Real robot motion is limited and easy to stop.
- No hardcoded MCP ports, host addresses, robot IPs, API keys, or secret tokens.
- New code does not assume ROS is required; DimOS can use multiple transports.
- MCP instructions say to start an MCP-enabled blueprint before calling `dimos mcp ...`.
- If the target robot is G1, use a G1-specific system prompt instead of a Go2-specific prompt.
- Tests start with replay/simulation where possible.

## When to use the included package files

- `resources/dimos_reference.md`: quick reference for DimOS concepts, CLI, MCP, skills, and testing.
- `resources/safety_and_testing.md`: safety gate and smoke-test sequence for replay, simulation, then real hardware.
- `templates/safe_motion_skill.py`: a safe wrapper pattern around a relative-move skill.
- `templates/skill_container_template.py`: minimal DimOS skill container.
- `templates/mcp_blueprint_template.py`: MCP-enabled blueprint skeleton.
- `templates/spec_protocol_template.py`: Spec/RPC injection pattern.
- `templates/system_prompt_patch.md`: example text to add to a robot system prompt.
- `scripts/scaffold_dimos_skill.py`: local helper for creating a new skill-container file.
