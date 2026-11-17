## Description:

OpenClaw digital-avatar onboarding system that guides an agent from a blank setup into a persona-driven assistant with memory scaffolding and anti-drift checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejianjun000](https://clawhub.ai/user/xiejianjun000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to onboard an agent through user-profile capture, persona setup, memory organization, skill recommendations, channel planning, and heartbeat-style drift checks. It is intended for configuring a personalized long-running assistant rather than a single task workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or maintain sensitive profile, secret, persona, and memory files.

Mitigation: Decide where USER.md, SECRET.md, SOUL.md, and .memory files will live before use, avoid storing passwords or tokens, and define retention and deletion rules.

Risk: The skill may recommend or install dependent skills without enough user control or privacy safeguards.

Mitigation: Review dependent skills before installation and approve only the skills needed for the intended workflow.

Risk: The skill is designed for a Chinese-language persona and long-term memory setup, which may not match every deployment.

Mitigation: Install only when that language and memory posture is intentional, and review generated persona and memory files before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejianjun000/skills/claw-taming)
- [README](artifact/README.md)
- [SOUL template](artifact/templates/SOUL_TEMPLATE.md)
- [Memory system template](artifact/templates/MEMORY_TEMPLATE.md)
- [Heartbeat inspection template](artifact/templates/HEARTBEAT_TEMPLATE.md)
- [Kaka growth-log example](artifact/examples/kaka-growth-log.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance and generated configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce USER.md, SECRET.md, SOUL.md, memory files, heartbeat reports, and skill or channel setup recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
