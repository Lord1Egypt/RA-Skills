## Description:

A ClawTip-based A2A article services skill that lets an agent create paid orders for hot-rank discovery, WeChat public-account draft publishing, and an end-to-end topic-to-article publishing workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucianaib0318](https://clawhub.ai/user/lucianaib0318)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operators, and public-account publishers use this skill to request paid article services through ClawTip: retrieving Chinese platform hot-rank topics, publishing Markdown content to a WeChat public-account draft, or running a paid end-to-end topic selection, article generation, and publishing flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send article instructions, order numbers, and payment credentials to a hardcoded remote HTTP service.

Mitigation: Use only with trusted operators, avoid submitting sensitive unpublished content or credentials beyond the intended payment credential, and review outbound network behavior before installation.

Risk: The skill can support automated public-account publishing.

Mitigation: Review generated article content and publishing intent before allowing a paid publish or full-auto workflow to proceed.

Risk: Order data is stored in local order files under the user's OpenClaw skills directory.

Mitigation: Protect local account storage and remove stale order files that contain order metadata or payment-related fields when they are no longer needed.

## Reference(s):

- [ClawTip](https://clawtip.jd.com)
- [ClawHub skill page](https://clawhub.ai/lucianaib0318/skills/a2a-article-services)
- [Publisher profile](https://clawhub.ai/user/lucianaib0318)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text responses with shell command output, order details, payment status, and service results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include order numbers, amounts, payment status, hot-rank content, article text, or publishing results after payment verification.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
