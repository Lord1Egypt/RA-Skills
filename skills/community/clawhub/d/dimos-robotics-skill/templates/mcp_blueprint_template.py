"""MCP-enabled DimOS blueprint template.

Replace the placeholder robot stack import with the stack you want to run.
Expose a module-level blueprint variable so `dimos run <name>` can discover it
when registered in DimOS.
"""

from __future__ import annotations

from dimos.agents.mcp.mcp_client import McpClient
from dimos.agents.mcp.mcp_server import McpServer
from dimos.core.coordination.blueprints import autoconnect

from .safe_motion_skill import SafeMotionSkill

# TODO: Import the robot stack you want to use, for example a replay/simulation
# stack while developing. Keep real-hardware IPs out of source code.
# from dimos.robot.unitree.go2.blueprints.agentic.unitree_go2_agentic import unitree_go2_spatial


safe_motion_agentic = autoconnect(
    # TODO: Add the robot stack first, for example: unitree_go2_spatial,
    McpServer.blueprint(),
    McpClient.blueprint(),
    SafeMotionSkill.blueprint(),
)
