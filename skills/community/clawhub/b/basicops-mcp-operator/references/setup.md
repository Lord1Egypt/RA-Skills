# BasicOps MCP setup checks

Use this reference when you need to determine whether BasicOps MCP is available, usable, and the right path for the request.

## Goal

Confirm the environment exposes a BasicOps MCP tool surface before doing any BasicOps work.

## What to look for

Look for either:
- tool names that clearly belong to BasicOps, for example names containing `basicops`
- an MCP server whose name clearly belongs to BasicOps
- per-workspace or per-profile BasicOps namespaces, for example `basicops-arla`, `basicops-inbox`, `basicops-ops`, or similar

Do not assume a single universal naming scheme. Match by clear BasicOps identity.

## Decision rule

### If BasicOps MCP is available and authenticated
Proceed with MCP.

### If BasicOps MCP is visible but appears unauthorized or incomplete
Say so briefly. Ask for setup or authentication instead of falling back to direct API calls.

Good pattern:
- "I can help with that, but this environment's BasicOps MCP connection is not ready yet. Once it is authenticated, I can operate the task directly."

### If no BasicOps MCP surface is available
State the prerequisite plainly and stop.

If the companion skill `basicops-mcp-setup` is available, hand off to it instead of improvising setup inside this operator skill.

Good pattern:
- "I can do that through BasicOps MCP, but this environment does not currently expose a BasicOps MCP server or BasicOps tools. Add that connection first, then I can operate the task directly."

## What not to do

- Do not silently switch to raw REST calls.
- Do not invent fake tool names.
- Do not pretend setup succeeded when the tool surface is missing.
- Do not probe unrelated servers looking for equivalent data.

## Minimal user explanation

Keep setup explanations short unless the user asks for more.

Preferred shape:
1. what is missing
2. why that blocks the request
3. what to add or authenticate

Example:
- "This skill expects a BasicOps MCP connection. I don't see one here yet, so I can't safely read or update your BasicOps data from this environment."
