## Description:

Manage AI agent skills using the @tiktok-fe/skills CLI (binary: ai-skills).

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanki-nn](https://clawhub.ai/user/nanki-nn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an agent find, install, update, remove, publish, and manage AI-agent skills across supported coding-agent environments with the @tiktok-fe/skills CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to run unpinned @tiktok-fe/skills tooling.

Mitigation: Use trusted and pinned package versions before allowing install or update commands.

Risk: Skill-management commands can make broad changes to future AI-agent behavior.

Mitigation: Review update lists before applying changes and limit commands to project scope or specific agents.

Risk: Force and auto-confirm flags can bypass useful confirmation steps for destructive operations.

Mitigation: Avoid blanket use of --force or -y and review cleanup, removal, and update actions before execution.

Risk: Install metadata may be uploaded when telemetry is enabled.

Mitigation: Disable telemetry when install metadata should not be uploaded.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nanki-nn/skills/323)
- [CLI Overview](llms/cli-overview.txt)
- [Add Command](llms/commands/add.txt)
- [Update Command](llms/commands/update.txt)
- [Clean Command](llms/commands/clean.txt)
- [Source Platforms Guide](llms/guides/source-platforms.txt)
- [Supported Agents Guide](llms/guides/agents-list.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command flags and review guidance for skill installation, update, publishing, and cleanup workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
