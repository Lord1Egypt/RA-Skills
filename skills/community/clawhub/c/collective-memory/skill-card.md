## Description:

Broadcast a single memory note to multiple AI-agent workspaces in one shot, upserting into MEMORY.md, AGENTS.md, TOOLS.md, USER.md, or another Markdown file across all targets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to broadcast a persistent Markdown memory note across multiple local agent workspaces and keep repeated broadcasts idempotent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently rewrite memory files across multiple workspaces.

Mitigation: Use explicit target lists, review every target before execution, and run with --dry-run when broadcasting to more than one workspace.

Risk: Sensitive notes could be copied into every selected memory file.

Mitigation: Do not broadcast secrets, account details, secret paths, tokens, passwords, API keys, or private keys.

Risk: Auto-discovery and custom filenames may select or write to unintended paths.

Mitigation: Prefer explicit --target arguments and confirm discovered workspaces and filenames before allowing writes.

Risk: Literal heading matching can update the wrong Markdown section when headings share broad tokens.

Mitigation: Use specific lookup keys, preview changes with --dry-run, and review target headings before updating existing sections.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songhonglei/skills/collective-memory)
- [Publisher profile](https://clawhub.ai/user/songhonglei)
- [Repository link from artifact documentation](https://github.com/Songhonglei/better-agent-skills)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Files, JSON]

**Output Format:** [Markdown guidance with bash command examples; script results are plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can update or preview Markdown memory files across one or more local workspaces.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
