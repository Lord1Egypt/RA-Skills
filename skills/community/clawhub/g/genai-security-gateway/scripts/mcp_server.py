from __future__ import annotations

from typing import Any

from guard_core import check_security_v2, optimize_prompt_v1


try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    try:
        from fastmcp import FastMCP
    except ImportError as exc:
        raise SystemExit(
            "An MCP server package is required. Install one with: "
            "python -m pip install 'mcp[cli]' or python -m pip install fastmcp"
        ) from exc


mcp = FastMCP("genai-security-gateway")


@mcp.tool()
def audit_prompt(message: str) -> dict[str, Any]:
    """Audit an LLM prompt for secrets, prompt injection, and semantic jailbreak risk."""
    return check_security_v2(message)


@mcp.tool()
def optimize_prompt(raw_input: str) -> dict[str, Any]:
    """Reserved optimization stub for future prompt dehydration and structured translation."""
    return optimize_prompt_v1(raw_input)


if __name__ == "__main__":
    mcp.run()
