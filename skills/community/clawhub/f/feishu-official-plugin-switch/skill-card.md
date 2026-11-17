## Description:

Guides OpenClaw users through switching from the community Feishu plugin to the official Feishu/Lark plugin with streaming output, user identity support, and expanded official tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to plan and execute a Feishu plugin migration, configure streaming output, switch plugin settings, restart the OpenClaw gateway, and check the resulting setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable npm installer commands can install unreviewed package versions, and examples include elevated execution patterns.

Mitigation: Pin the @larksuite/openclaw-lark-tools package to a reviewed version, verify the package source and registry, and avoid elevated privileges unless independently required.

Risk: Plugin switching and gateway restart steps can interrupt the Feishu bot or overwrite working OpenClaw settings.

Mitigation: Back up OpenClaw configuration, schedule a maintenance window, and verify plugin state after restart before relying on the migrated bot.

Risk: Requested Feishu/Lark user permissions can allow broad read and write access to workspace content.

Mitigation: Grant only the permissions needed for the intended workflow and complete user authorization only after reviewing workspace data-access implications.

Risk: The artifact reports success in guided steps without independently proving that each external change has occurred.

Mitigation: Run the documented doctor, info, and plugin-list checks after each change and treat success messages as guidance until verified in the local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rfdiosuao/skills/feishu-official-plugin-switch)
- [Official Feishu/Lark plugin guide](https://bytedance.larkoffice.com/docx/MFK7dDFLFoVlOGxWCv5cTXKmnMh)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw Lark tools repository](https://github.com/larksuite/openclaw-lark)
- [Artifact-linked skill repository](https://github.com/rfdiosuao/openclaw-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status messages with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns step status, next-action hints, diagnostic guidance, and manual commands for OpenClaw and npm-based plugin tooling.]

## Skill Version(s):

3.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
