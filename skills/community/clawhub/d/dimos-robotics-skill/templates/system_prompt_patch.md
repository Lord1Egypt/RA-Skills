# System Prompt Patch for a New DimOS Skill

Add a concise entry like this to the robot-specific `# AVAILABLE SKILLS` section. Keep it factual and match the actual MCP tool name and parameters.

```text
safe_relative_move(forward: float = 0.0, left: float = 0.0, degrees: float = 0.0) -> str
Use this only for small, validated relative movements. The skill refuses commands above its configured safety limits. Prefer observation and planning before movement.
```

Prompt hygiene:

- Do not list skills that are not present in `dimos mcp list-tools`.
- Use the robot-specific prompt for the target platform.
- Describe limits and refusal behavior so the agent understands failed calls.
- Keep parameter descriptions short; the full skill docstring also appears in tool metadata.
