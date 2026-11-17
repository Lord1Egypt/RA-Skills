## Description:

Feelslikeclaude is a local-only OpenClaw behavior overlay that makes the agent more proactive, calm, concise, and execution-focused without changing identity files or using network activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whooshinglander](https://clawhub.ai/user/whooshinglander)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to make OpenClaw responses more direct, action-first, and follow-through oriented while preserving existing safety constraints and identity boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make the agent more action-oriented and less likely to ask for confirmation on routine reversible work.

Mitigation: Keep confirmations for destructive, public, external, credentialed, or otherwise high-impact actions, as required by the artifact guardrails.

Risk: Users could misread the skill name as an identity change.

Mitigation: The artifact explicitly says this is a style overlay and instructs the agent not to claim to be Claude or rewrite personality/config files unless asked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whooshinglander/skills/feelslikeclaude)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown behavior instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-only style overlay; no API calls, package installation, executable payloads, or automatic identity-file changes.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
