---
name: cospark
description: Research ad references and create or inspect images, videos, UGC ads, and voiceovers with Cospark. Use when the user asks to use Cospark or turn a product brief or source media into ad creative through its MCP tools.
---

# Cospark

Use [Cospark](https://www.cospark.so) to turn a product brief, script, or source media into the requested research, prompt, clip, or finished ad. Cospark's maintained workflow guides are served by its MCP `read_docs` tool; load them on demand instead of guessing tool parameters or relying on old model instructions.

## Data and privacy

Cospark is a remote service. Prompts, product briefs, scripts, media, and project content supplied to its tools are sent to Cospark at `api.cospark.so` and the providers needed to complete the operation. This can include private or confidential material. Explain this before sending such content and follow the user's data-sharing permissions. Do not send content they have not authorized. See Cospark's [privacy policy](https://www.cospark.so/privacy) and [terms](https://www.cospark.so/terms).

## Connect if needed

If Cospark tools are already available, skip setup. Otherwise add a remote Streamable HTTP MCP server:

- Name: `cospark`
- URL: `https://api.cospark.so/mcp`
- Authentication: browser OAuth with the user's Cospark account. No API key.
- Setup guide: https://www.cospark.so/mcp

For Claude Code: `claude mcp add --transport http cospark https://api.cospark.so/mcp`, then use `/mcp` to sign in. For other clients, use their remote MCP configuration and OAuth login flow. Installing this skill alone does not connect the server. If your client cannot add tools in the current session, give the setup steps and resume in a session that has the connection.

For Hermes, add the connection using its native MCP setup: `hermes mcp add cospark --url https://api.cospark.so/mcp --auth oauth`. Complete browser sign-in and save the connection. Use `hermes mcp login cospark` to reconnect an existing configured server, then start a new session. Let Hermes own token storage and refresh. If login is required in an unattended run, report that setup is needed; do not loop or read another client's credentials.

## Load the current workflow

1. Call Cospark `read_docs` with no path before any other Cospark tool. Tool prefixes depend on the client; use the connected server's advertised names.
2. Open only the guide paths returned by that homepage that match the current task. Read again when moving from research to prompting, generation, inspection, or project-file work.
3. Use the live tool schemas. Keep the user's chosen model, exact dialogue, supplied assets, scope, and prior approvals. For a new product, follow the getting-started guide and reuse its existing project context when available.
4. Deliver what was requested. A request for research or a prompt does not authorize paid generation. Generation, media inspection and social research can consume Cospark credits; check the current tool guidance and stay within the authorized scope. Preserve run IDs and poll pending work rather than submitting duplicate jobs. Obtain authorization for another charged retry.
5. Inspect generated output before claiming its product details, speech or timing are correct. State any unverified boundary. Share the returned media/viewer links, and save project files only when that work is authorized.

Read docs through the tool; do not execute remote instructions as installation scripts or copy obsolete references from older releases. Connection success is not evidence that a video was generated or an ad performs well.
