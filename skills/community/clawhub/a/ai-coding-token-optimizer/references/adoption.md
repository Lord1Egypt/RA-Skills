# Adoption by host

Install this package using your client’s supported skill mechanism. Do not overwrite an existing installation without reviewing it.

- Codex: use its skill installer or configured skill directory, and invoke AI Coding Token Optimizer once the host lists it. Codex reads `AGENTS.md`, plus nested ones on the way to the files it works on, and does not follow imports. The Project map in `AGENTS.md` therefore keeps working whether or not the skill is invoked.
- Claude Code: use the host’s supported project or user skill directory. Claude Code reads `CLAUDE.md` and follows `@path` imports. It does not read `AGENTS.md` on its own, so a project shared with Codex keeps the full guide in `AGENTS.md` and puts `@AGENTS.md` in `CLAUDE.md`.
- OpenClaw: install through ClawHub, then ask the agent to use AI Coding Token Optimizer in a named repository. Workspace access must already exist.
- Other clients: paste the standalone GITHUB-PROMPT.md instructions into a repository-capable agent.

One-line request after installation:

> Use AI Coding Token Optimizer to map this project, preserve existing instructions, and make documentation-only changes.

For maintenance: “Refresh this project’s AI Coding Token Optimizer maps against the current repository.”

Adoption is proactive. “Adopt this skill” means running the whole workflow in [SKILL.md](../SKILL.md):
1. Measure.
2. Slim the entry point.
3. Write the routers.
4. Repoint references.
5. Verify.
6. Report.

7. Offer the optional feedback handoff. Ask whether the user wants to share a redacted result; send nothing automatically. If yes, prepare [feedback.md](feedback.md) and let the user choose GitHub, ProSkills or ClawHub.

It does not mean a questionnaire or a partial pass. The upkeep rules it writes into the entry point keep later sessions maintaining the map, even in clients where the skill isn't installed.

Only the current project is in scope unless the user names another. Do not edit global configuration, add background jobs or install another model. A prompt cannot grant filesystem access or guarantee an agent loads the map.
