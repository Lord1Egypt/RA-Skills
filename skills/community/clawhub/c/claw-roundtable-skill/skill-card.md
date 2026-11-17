## Description:

RoundTable v3.0 is a multi-agent roundtable discussion engine for structured proposal review using heterogeneous model routing, MMR intent parsing, convergence control, and a 170+ expert library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krislu1221](https://clawhub.ai/user/krislu1221)

### License/Terms of Use:

MIT

## Use Case:

Developers, product teams, and decision makers use this skill to run a structured multi-agent review of technical plans, product proposals, and complex decisions. It produces adversarial critique, revised recommendations, and an execution-oriented plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags costly remote sub-agent work after only a confirmation prompt.

Mitigation: Require an explicit confirmation gate before execution and use the skill only when multi-agent remote work is expected.

Risk: The security scan flags default private OpenClaw configuration file discovery.

Mitigation: Use explicit model configuration instead of default private config discovery, especially in sensitive environments.

Risk: Topics and generated discussion summaries may be persisted, broadcast to chat, or sent as notifications when those features are enabled.

Mitigation: Use non-secret topics and keep chat broadcasting, notifications, and report persistence disabled for sensitive discussions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krislu1221/skills/claw-roundtable-skill)
- [OpenClaw RoundTable Documentation](https://docs.openclaw.ai/skills/roundtable)
- [Prompt Framework](artifact/prompts/framework.md)
- [Model Configuration](artifact/MODEL_CONFIG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown reports, JSON reports, structured tables, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally persist discussion reports and send progress notifications when those features are enabled.]

## Skill Version(s):

3.0.13 (source: ClawHub release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
