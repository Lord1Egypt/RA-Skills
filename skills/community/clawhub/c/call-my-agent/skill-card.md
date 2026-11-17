## Description:

Create a private phone line between a user and an OpenClaw agent, using local OpenClaw auth profiles and Tailscale instead of Twilio or rented phone numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrbese](https://clawhub.ai/user/mrbese)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to set up, configure, and verify a private internet voice line for one local OpenClaw agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run local code from a referenced package that was not included in the reviewed artifact or pinned immutably.

Mitigation: Confirm the exact ClawHub package version or commit before installation, review setup scripts, and approve package install commands before they run.

Risk: Persistence files or Tailscale Serve routes can expose a long-running local service if enabled without review.

Mitigation: Require explicit confirmation before enabling persistence or remote access, bind locally by default, and provide teardown commands for each enabled route or service.

Risk: OpenAI API keys could be exposed if requested, printed, pasted, or stored outside the expected local auth flow.

Mitigation: Use existing OpenClaw auth profiles first, never print or store keys in chat, and use OpenClaw's local auth flow if a new key is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrbese/skills/call-my-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with command snippets, configuration steps, and verification results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes privacy checks and explicit confirmation gates for install, persistence, and remote access actions.]

## Skill Version(s):

0.1.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
