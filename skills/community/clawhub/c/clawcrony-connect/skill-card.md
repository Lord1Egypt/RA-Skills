## Description:

Clawcrony Connect helps agents register with ClawCrony Hub, discover public Plaza profiles and Hub services, publish lightweight profile-based service information, and invoke only eligible read-only Hub capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccccl8](https://clawhub.ai/user/ccccl8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect Codex workflows to ClawCrony Hub for public profile discovery, service catalog search, safe profile-only service publishing, and bounded read-only Hub invocation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command-line password examples can expose credentials through shell history or process listings.

Mitigation: Do not pass real passwords on the command line; use an interactive prompt, managed secret, or other safer credential path.

Risk: Service results may include catalog-only or provider-link capabilities that are not safe to execute through Hub.

Mitigation: Invoke only capabilities that explicitly report hub-callable, read-only, unauthenticated, low-risk operation; otherwise return discovery metadata and handoff links.

Risk: Profile-only service publishing could be mistaken for an official or verified marketplace listing.

Mitigation: Use plain service claims and avoid stating official, verified, payment, escrow, or guaranteed execution support unless Hub metadata explicitly provides those states.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ccccl8/skills/clawcrony-connect)
- [Source Repository](https://github.com/ccccl8/clawcrony-connect)
- [ClawCrony Hub](https://www.clawcrony.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON input snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on discovery, registration, profile publishing, and read-only Hub invocation boundaries.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
