## Description:

Generates promotional social media content for GitHub bounty campaigns using repository details and custom messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vut08905](https://clawhub.ai/user/vut08905)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and campaign maintainers use this skill to draft social posts that promote GitHub bounty campaigns from repository metadata and optional custom messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub and social-platform tokens may be over-scoped or exposed during setup.

Mitigation: Use least-privilege tokens, test with noncritical accounts, and avoid granting publishing credentials until the installed behavior is verified.

Risk: Public campaign posts may misstate repository or bounty details.

Mitigation: Review generated text before publication and confirm repository metadata, bounty terms, and platform requirements.

Risk: Dependencies include vulnerable HTTP components according to the security evidence.

Mitigation: Update or pin dependencies before relying on this skill in a production workflow.

Risk: The current artifact logs post text rather than actually posting to a social platform.

Mitigation: Verify social-platform integration behavior before granting social credentials or depending on automated publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vut08905/skills/autopost-github-bounty)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with command examples and generated social post text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses repository metadata and optional custom message input; current artifact logs generated post text rather than calling a social-platform API.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
