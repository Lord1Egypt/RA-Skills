## Description:

Manage Discord workspace structure and OpenClaw routing as code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofan](https://clawhub.ai/user/ofan)

### License/Terms of Use:


## Use Case:

Developers and workspace administrators use Disclaw to define, validate, preview, apply, import, and roll back Discord server structure and OpenClaw agent-to-channel bindings from a YAML configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to globally install an unpinned external npm tool.

Mitigation: Use a pinned and trusted version of @ofan/disclaw where possible before installation.

Risk: The tool handles Discord and OpenClaw credentials.

Mitigation: Grant the Discord bot and OpenClaw gateway only the minimum permissions needed for the intended server and channels.

Risk: The tool can change or delete Discord server structure.

Mitigation: Run validation, diff, or dry-run first, and review uses of --yes and --prune before applying changes.

## Reference(s):

- [Disclaw on ClawHub](https://clawhub.ai/ofan/skills/disclaw)
- [Publisher profile: ofan](https://clawhub.ai/user/ofan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with YAML, JSON, and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include validation, diff, dry-run, apply, import, rollback, and troubleshooting command sequences.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
