## Description:

Automates Vietnamese ads-management interactions in Telegram and chat by routing reports, alerts, proposals, competitor checks, and daily planning for a boss user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phap1106](https://clawhub.ai/user/phap1106)

### License/Terms of Use:

MIT-0

## Use Case:

External ads operators and business users can use this skill to make an agent respond to boss messages with immediate advertising reports, alerts, budget proposals, competitor checks, and next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent toward broad automatic authority over sensitive advertising workflows.

Mitigation: Limit activation to explicit ads-management commands and require confirmation before approvals, writes, publishing, or Meta setting changes.

Risk: Weak scoping and free-form saved instructions can cause unintended persistent behavior.

Mitigation: Review stored instructions, constrain them to the intended ad account and workflow, and remove stale or ambiguous instructions before deployment.

Risk: Credential setup guidance could expose access tokens if handled in chat or skill text.

Mitigation: Move access-token setup to a secure settings flow and avoid storing credentials in free-form messages or skill files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phap1106/skills/ads-claw3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain-text chat responses with inline commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Vietnamese by default, with concise reports, alerts, proposal recommendations, and concrete next actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
