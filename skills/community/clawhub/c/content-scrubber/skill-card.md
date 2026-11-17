## Description:

OpenClaw plugin that scrubs private infrastructure details from outgoing messages with regex-based redaction of RFC 1918 IPs, localhost ports, SSH targets, and hostnames before they reach Discord, Telegram, Signal, or other messaging surfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to reduce accidental disclosure of private infrastructure details in outgoing chat messages. It is intended for message-sending workflows where deterministic text replacement is acceptable as a best-effort privacy control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scrubber is a best-effort privacy control and may miss sensitive endpoint formats, internal hostnames, SSH targets, or localhost representations outside its built-in regex rules.

Mitigation: Test representative sensitive formats before deployment and extend or tune the rules for the environment's actual message patterns.

Risk: Dry-run mode and allowed recipients can bypass redaction for real outgoing messages.

Mitigation: Keep dryRun disabled for protective use and restrict allowedRecipients to explicitly reviewed destinations.

## Reference(s):

- [Content Scrubber ClawHub Release](https://clawhub.ai/solomonneas/skills/content-scrubber)
- [solomonneas ClawHub Profile](https://clawhub.ai/user/solomonneas)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript plugin code and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deterministic replacement text such as [redacted-ip], [redacted-service], [redacted-target], and [redacted-host].]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
