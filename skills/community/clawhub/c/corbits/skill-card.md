## Description:

SECURITY PROOF OF CONCEPT - NOT the real Corbits skill. Placeholder published to demonstrate that the unclaimed ClawHub slug "corbits", referenced by moonpay/skills (corbits-marketplace), can be claimed by anyone. Reported to MoonPay via HackerOne. Does nothing.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[tumbwa](https://clawhub.ai/user/tumbwa)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users can use this PoC to recognize that a skill published under the corbits slug is a placeholder, not the real Corbits skill. It also provides an install marker for checking the PoC and warns users not to share secrets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users or agents could mistake this placeholder for the real Corbits skill because it uses the same ClawHub slug.

Mitigation: Treat it only as a security PoC, confirm the publisher and listing, and check the install marker before relying on a Corbits skill.

Risk: The skill provides guidance about handling secrets and an install-verification marker that should be reviewed before installation.

Mitigation: Review the stated secret-handling guidance and marker, and never export or paste a private key, seed phrase, or API key.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/tumbwa/skills/corbits)
- [Publisher profile](https://clawhub.ai/user/tumbwa)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown text with a verification marker and safety guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No commands, scripts, or network access; the artifact says the skill does nothing beyond its stated guidance and marker.]

## Skill Version(s):

0.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
