## Description:

Remote Browser automation via CUA (Computer Use Agent). Use when user requires remote browser to do anything.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallcosmos](https://clawhub.ai/user/smallcosmos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to forward exact user browser automation tasks to a Computer Use Agent for navigation, search, form interaction, screenshots, scraping, and related browser workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill forwards raw user requests to an external computer-use agent for browser automation, including potentially sensitive login or checkout flows.

Mitigation: Use an isolated browser profile and non-sensitive tasks unless the CUA wrapper, SDK environment, network destinations, logging, and confirmation controls have been independently reviewed.

Risk: Raw pass-through prompts can trigger actions involving passwords, payment details, private account data, or irreversible transactions.

Mitigation: Do not send passwords, payment details, private account data, or irreversible actions through raw pass-through prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallcosmos/skills/computer-use-skill)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Text results stream with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pass-through browser automation requests are sent without task modification.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
