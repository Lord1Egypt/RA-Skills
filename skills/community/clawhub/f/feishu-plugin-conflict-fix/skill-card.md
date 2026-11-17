## Description:

Provides troubleshooting guidance for Feishu and OpenClaw plugin conflicts, TTS message attachments, and multi-bot tool isolation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose Feishu tool-name conflicts, disable unwanted TTS behavior, isolate tools across multiple bots, and recover OpenClaw Feishu configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recovery steps include deleting Feishu plugin files and resetting OpenClaw configuration, which can remove working settings if paths or backups are wrong.

Mitigation: Run diagnostic commands first, verify exact paths, and confirm a restorable backup before using reset or deletion commands.

Risk: The guidance recommends installing a package with npx, which can execute package code during installation.

Mitigation: Pin and verify the package source and version before running npx installation commands.

Risk: Recommended Feishu plugin capabilities may require document write access or message-history permissions.

Mitigation: Grant only the Feishu document or message-history permissions that are required for the intended workflow.

## Reference(s):

- [Official Feishu Plugin Guide](https://my.feishu.cn/docx/MFK7dDFLFoVlOGxWCv5cTXKmnMh)
- [Feishu Streaming Reply Configuration](https://www.feishu.cn/docx/Qv3fdMljgoUjYJx5cwAc3tinnfc)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes diagnostic steps, OpenClaw configuration examples, and recovery command sequences.]

## Skill Version(s):

1.0.0 (source: release metadata, skill.json, artifact version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
