## Description:

Provides basic blockchain safety checks for agents, including Ethereum and Base address reputation checks, token honeypot detection, and free quota lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to run basic pre-transaction checks on Ethereum and Base addresses or tokens and to monitor free API quota. Results should support, not replace, human review for high-value or ambiguous blockchain decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad command execution despite primarily describing API lookup workflows.

Mitigation: Review the skill before deployment, restrict use to documented Ethereum and Base read-only checks, and avoid running unrelated shell commands from the skill.

Risk: Quota tracking may send a client fingerprint or fall back to IP/User-Agent data.

Mitigation: Use a non-sensitive client fingerprint, avoid embedding secrets or personal data in request headers, and document fingerprint privacy handling for users.

Risk: Blockchain safety lookups can be incomplete or uncertain and do not guarantee that a transaction or token is safe.

Mitigation: Require human review before acting on medium, high, critical, high-value, or ambiguous results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/aegis-security-free)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-style API response examples and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include quota status, risk levels, threat signals, and API request guidance; the free tier is limited to Ethereum and Base.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter version is 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
