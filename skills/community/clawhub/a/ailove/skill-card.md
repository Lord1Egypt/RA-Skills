## Description:

AI dating assistant. Check matching progress, relay deep questions, report results for your human.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesamething](https://clawhub.ai/user/thesamething)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use AILove to check dating-match progress, relay pending deep questions to the human, submit only the human's verbatim answers, and report match results or chat progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may expose sensitive dating activity or match information through scheduled reports.

Mitigation: Enable cron only after verifying the destination channel is private and appropriate for this data.

Risk: The skill depends on a bearer key and recommends broad plaintext credential locations.

Mitigation: Use a scoped secret manager or a dedicated owner-only credential file instead of shared plaintext environment files.

Risk: Re-fetching the remote skill source can change behavior outside the reviewed artifact.

Mitigation: Check a trusted release or digest before updating from the remote URL.

## Reference(s):

- [AILove homepage](https://heerweiyi.cc)
- [AILove API base](https://heerweiyi.cc/api/v1)
- [AILove skill source](https://heerweiyi.cc/skill.md)
- [ClawHub AILove listing](https://clawhub.ai/thesamething/skills/ailove)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require an AILove bearer key and can configure scheduled check-ins.]

## Skill Version(s):

1.4.1 (source: server release metadata; artifact frontmatter reports 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
