## Description:

Turn authorized community event site photos and office-supplied facts into one silent 2–15-second site photo clip per photo, in capture order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Community site teams use this skill to turn approved event photos and office-supplied facts into an ordered set of short, silent site clips, one clip per photo.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shared Beatra authorization requests account permissions beyond silent video work, including voice management.

Mitigation: Prefer a version with permissions limited to video work and review the shared authorization before installing.

Risk: Selected event photos are sent for external processing, and installation and system details are reported periodically.

Mitigation: Use only photos approved for external processing and account for the periodic installation and system reporting.

Risk: Video requests have a batch cost.

Mitigation: Confirm the quoted batch cost before submitting.

## Reference(s):

- [Community site one-shot workflow](artifact/references/workflow.md)
- [Updates and security](artifact/references/updates-and-security.md)
- [Beatra MCP service](https://mcp.beatra.ai/mcp)
- [ClawHub skill release](https://clawhub.ai/beatra-ai/skills/community-site-clip)

## Skill Output:

**Output Type(s):** [Video clips, Text]

**Output Format:** [Silent 2–15-second video clips, with a text plan and result details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One clip per photo, returned in capture order; result details include dimensions, duration, usage, and charged credits.]

## Skill Version(s):

0.2.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
