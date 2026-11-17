## Description:

Minimal demonstration skill for verifying a ClawHub publish flow by printing a configurable greeting and the current date.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release maintainers use this demonstration skill to smoke-test ClawHub publishing, installation, rendering, and skill input/output documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The referenced demo-hello-skill command may not exist in the target environment.

Mitigation: Confirm the command is installed and available on PATH before relying on the skill for publish or install smoke tests.

Risk: The skill is intended for demonstration and publish-flow validation rather than production automation.

Mitigation: Use it for controlled smoke tests and review any adaptation before deploying it into operational workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/demo-hello-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with bash command examples and single-line stdout text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Greeting recipient can be customized with --to; output includes an ISO-8601 date.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
