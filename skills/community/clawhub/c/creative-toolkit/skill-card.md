## Description:

Find visual inspiration, generate or edit images and videos, and use the user's MeiGen favorites, boards and characters through the connected remote MCP. Use for MeiGen requests; preserve the user's existing creative choices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jau123](https://clawhub.ai/user/jau123)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use MeiGen to discover visual references, create or edit images and videos, and work with their MeiGen favorites, boards, history, assets, and characters through an authenticated remote connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The linked remote connection plugin was not included in the security assessment of the inspected skill files.

Mitigation: Review the plugin and its permissions separately before installing or enabling it.

Risk: Image and video generation uses purchased MeiGen credits, and a failed or interrupted response may not establish whether a job started or credits were charged.

Mitigation: Check live prices, keep the original request ID and inputs, and query that job's status before considering another submission.

Risk: Non-public reference material sent to the remote service may be exposed through public links or uploads.

Mitigation: Explain the exposure and obtain authorization before uploading non-public material; use real accessible URLs or supported uploads.

## Reference(s):

- [MeiGen MCP and OpenClaw information](https://www.meigen.ai/mcp?tab=openclaw)
- [MeiGen remote connection plugin](https://clawhub.ai/plugins/meigen-ai-design)
- [Connection and migration guide](references/connection.md)
- [Troubleshooting guide](references/troubleshooting.md)
- [MeiGen MCP migration guide](https://github.com/jau123/MeiGen-AI-Design-MCP/blob/main/MIGRATION.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Images, Videos]

**Output Format:** [Text responses and returned image or video media]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media availability, previews, and downloads depend on the remote tools and host support.]

## Skill Version(s):

4.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
