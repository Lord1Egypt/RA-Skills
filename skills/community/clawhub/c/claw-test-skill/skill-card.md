## Description:

Test skill created and published directly via ClawHub API using provided key. Use when testing ClawHub publish flow from agents or Grok.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maliot100x](https://clawhub.ai/user/maliot100x)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to verify that ClawHub skill publishing and registry loading work for a test release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user may install the test skill expecting production functionality.

Mitigation: Confirm the package name and intended test purpose before installing; the skill only reports publish success and suggests install commands.

Risk: The skill references publishing with an API key in its notes, which could be mistaken for a request to provide credentials.

Mitigation: Do not provide credentials to this skill; evidence.security states it does not request credentials, execute code, collect data, or persist changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maliot100x/skills/claw-test-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/maliot100x)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No side effects; reports publish success and suggests install commands.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
