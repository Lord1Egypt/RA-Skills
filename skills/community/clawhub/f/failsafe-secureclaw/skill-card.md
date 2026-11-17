## Description:

Native security prompts and best practices to instantly make your OpenClaw instance safer without relying on 3rd party APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sooyoon-eth](https://clawhub.ai/user/sooyoon-eth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add prompt-based security guardrails for OpenClaw, including supply-chain review prompts, indirect prompt-injection handling, exfiltration checks, sandboxing guidance, and jailbreak resistance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill changes agent behavior by adding broad security guardrail instructions.

Mitigation: Review the prompt guidance before installation and confirm it matches the intended agent policy and operating environment.

Risk: The artifact documentation overstates included companion files such as PROMPTS.md, TOOL_SAFETY.md, INCIDENT_RESPONSE.md, and BEST_PRACTICES.md.

Mitigation: Rely only on files present in the released artifact unless the publisher supplies a complete package with the missing companion files.

Risk: Prompt-only guardrails depend on the local model following instructions and should not be treated as a complete security control.

Mitigation: Keep platform sandboxing, tool permissions, secret handling, and human review controls in place alongside the skill.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sooyoon-eth/skills/failsafe-secureclaw)
- [Failsafe Security homepage](https://getfailsafe.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown prompt guidance and configuration review instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only security guidance; no executable payload, network code, or hidden persistence reported by security evidence.]

## Skill Version(s):

1.0.5 (source: release evidence, SKILL.md frontmatter, package.json, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
