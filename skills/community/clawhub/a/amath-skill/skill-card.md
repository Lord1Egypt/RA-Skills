## Description:

Discover the Socthink 奥数 learning system through curriculum trees, topic/problem lookup, Socratic tutoring, and quiz flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[star8592](https://clawhub.ai/user/star8592)

### License/Terms of Use:

MIT-0

## Use Case:

External users, OpenClaw users, and agent-tool developers use this skill to explore the Socthink math learning product through curriculum discovery, topic and problem lookup, Socratic tutoring flows, and quiz entry points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passwords and bearer tokens may be exposed through command lines, transcripts, or in-process session state.

Mitigation: Use isolated test accounts, avoid real credentials in command lines or shared transcripts, pass tokens only in controlled sessions, and clear the in-process session after use.

Risk: Installer guidance includes a curl-to-bash OpenClaw setup path.

Mitigation: Independently review and verify installer URLs before execution, especially on shared or sensitive machines.

Risk: A local .env file can hold a default bearer token.

Mitigation: Keep .env files out of source control and use short-lived or test tokens for demonstrations.

## Reference(s):

- [Socthink product homepage](https://amath.socthink.cn)
- [ClawHub skill listing](https://clawhub.ai/star8592/skills/amath-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some quiz and personalized recommendation flows require bearer-token authentication.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
