## Description:

Helps agents discover installable crypto, DeFi, blockchain, and trading skills and present search and installation guidance to users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youhualan](https://clawhub.ai/user/youhualan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover crypto-related skills, map user intent to Skills CLI searches, and present install options with security reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing remote crypto or trading skills globally and non-interactively can introduce unreviewed code or misleading automation into sensitive workflows.

Mitigation: Review the skill source before installation, prefer pinned versions, use local or sandboxed installation, and require explicit confirmation before adding trading-related skills.

Risk: Crypto workflows can expose wallet seed phrases, withdrawal-capable exchange keys, or production trading credentials if installed skills are granted broad access.

Mitigation: Do not run this skill on systems or accounts that hold seed phrases or withdrawal-capable keys; use narrowly scoped trade-only credentials when credentials are needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youhualan/skills/find-crypto-skills)
- [Skills directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces suggested Skills CLI search and install commands; does not directly execute trades.]

## Skill Version(s):

1.0.0 (source: target metadata and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
