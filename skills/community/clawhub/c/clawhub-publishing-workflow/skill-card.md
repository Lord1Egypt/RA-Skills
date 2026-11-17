## Description:

Complete workflow for publishing OpenClaw skills to ClawHub, including authentication troubleshooting, skill preparation, publishing, and verification guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stefanferreira](https://clawhub.ai/user/stefanferreira)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to publish new or updated OpenClaw skills to ClawHub, verify authentication, prepare release structure, and troubleshoot common publishing failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill discusses stealth browser and residential proxy tactics for authentication bot checks.

Mitigation: Prefer documented token authentication with `clawhub login --token --no-browser`; avoid stealth browser or residential proxy approaches unless ClawHub and relevant providers explicitly authorize that use.

Risk: The workflow recommends installing the ClawHub CLI globally before publishing.

Mitigation: Pin and verify the ClawHub CLI package before global installation, and review the skill before installing or executing commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stefanferreira/skills/clawhub-publishing-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces publishing workflow guidance, command examples, validation steps, and troubleshooting notes.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
