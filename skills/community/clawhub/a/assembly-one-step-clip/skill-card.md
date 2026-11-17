## Description:

Turns authorized stills and seller-supplied step facts into one assembly-step video per still.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Seller and listing teams use the skill to turn authorized, ordered assembly-step stills and seller-supplied facts into short instructional clips, one per still.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared authorization also grants audio and voice permissions beyond the video workflow; uploaded images leave the computer and recurring installation analytics are sent.

Mitigation: Review the permission scope before approval, upload only authorized stills, and account for recurring installation analytics.

Risk: Uninstalling can disconnect other Beatra skills that rely on the shared account connection.

Mitigation: Check for other installed Beatra skills before uninstalling, and revoke access through the Beatra Console when appropriate.

## Reference(s):

- [ClawHub release](https://clawhub.ai/beatra-ai/skills/assembly-one-step-clip)
- [Publisher profile](https://clawhub.ai/user/beatra-ai)
- [Assembly one-step workflow](artifact/references/workflow.md)
- [Updates and security](artifact/references/updates-and-security.md)
- [Beatra MCP service](https://mcp.beatra.ai/mcp)

## Skill Output:

**Output Type(s):** [Video, Text]

**Output Format:** [One short generated video clip per still, plus a labeled step plan and delivery summary]

**Output Parameters:** [One clip per assembly step, delivered in step order]

**Other Properties Related to Output:** [Clips remain separate and are not stitched together.]

## Skill Version(s):

0.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
