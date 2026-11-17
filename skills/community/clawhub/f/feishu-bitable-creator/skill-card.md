## Description:

Create and populate Feishu (Lark) Bitable multidimensional tables with automated cleanup, field creation, record insertion, primary field naming, and owner admin setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaowanqi08141999](https://clawhub.ai/user/gaowanqi08141999)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to create clean Feishu Bitables from structured data, add useful fields and records, and assign the intended human owner as an administrator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates Feishu Bitables and can grant full admin access on created tables to a provided open_id.

Mitigation: Confirm the owner open_id before use and grant admin access only to the intended user.

Risk: The required Feishu app permissions allow Bitable creation and document permission management in the configured workspace.

Mitigation: Install only when those Feishu app permissions are acceptable for the workspace and credentials are managed through the configured Feishu channel.

## Reference(s):

- [OpenClaw Feishu Channel Documentation](https://docs.openclaw.ai/channels/feishu)
- [Feishu Developer App Console](https://open.feishu.cn/app)
- [ClawHub Skill Page](https://clawhub.ai/gaowanqi08141999/skills/feishu-bitable-creator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript examples, JSON configuration snippets, and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu Bitable URLs, table identifiers, field names, cleanup counts, record counts, and owner permission status.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
