## Description:

Agentspace helps developers share and observe a named AI development workspace through live browser links, CLI commands, and dev HTTP API guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to start, inspect, share, and troubleshoot live AI-agent development folders, including generated files, logs, build output, tests, and handoff state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run the mutable latest version of the Agentspace CLI through npm.

Mitigation: Use a pinned, reviewed ascli version before running sync or share commands.

Risk: The CLI uploads the named development folder and can create editable share links.

Mitigation: Confirm the exact path before syncing or sharing, and use view-only links unless edit access is required.

Risk: .ascli.json can contain workspace claim tokens.

Mitigation: Treat claim tokens as sensitive and do not commit .ascli.json or any file containing claim tokens.

## Reference(s):

- [Agentspace homepage](https://agentspace.so)
- [Agentspace CLI package](https://www.npmjs.com/package/@agentspace-so/ascli)
- [Agent Space Commands](references/commands.md)
- [Developer reference for agentspace dev sessions](references/developer.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks and URLs returned by the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent should only return URLs printed by ascli and should confirm the exact target path before sync or share operations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
