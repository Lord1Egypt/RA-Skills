## Description:

AI-powered email subject line generator. Create subject lines that get opened.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icepopma](https://clawhub.ai/user/icepopma)

### License/Terms of Use:

MIT

## Use Case:

External users and marketers use this skill to generate multiple email subject line options for launches, newsletters, sales, and announcements through the OpenClaw Sloan agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal invocations attempt a SkillPay charge unless test mode is used, and the source includes a shared-looking merchant key.

Mitigation: Review the payment flow before use, avoid relying on the embedded key, and run in test mode or a controlled environment until billing behavior is confirmed.

Risk: The documented install path is mutable and dependencies resolve through an HTTP mirror in the lockfile.

Mitigation: Prefer pinned package and dependency sources, verify package integrity, and review dependencies before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/icepopma/skills/email-subject-generator)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Numbered plain text subject-line options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically returns 10 subject lines; normal invocation attempts a pay-per-use charge unless test mode is used.]

## Skill Version(s):

1.1.2 (source: server release metadata and package.json; SKILL.md frontmatter says 1.0.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
