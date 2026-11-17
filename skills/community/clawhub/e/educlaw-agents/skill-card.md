## Description:

Multi-agent tutoring skill that routes learners to isolated English and math subject agents, with Chinese routing configured as coming soon.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[xiaohuiing](https://clawhub.ai/user/xiaohuiing)

### License/Terms of Use:

MIT-0

## Use Case:

Learners, educators, and skill developers use this package to test OpenClaw-style routing across subject-specific tutoring agents with isolated conversation memory. The packaged experience focuses on elementary English and math practice, while Chinese is configured as a coming-soon route.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Math access control uses documented test activation codes and conversation memory, which is not reliable paid access enforcement.

Mitigation: Use this release for testing only, or move entitlement checks and activation validation to a trusted service before offering paid access.

Risk: Chinese subject routing is configured while the corresponding subject agent is marked as coming soon.

Mitigation: Keep Chinese routing disabled or present it as unavailable until the Chinese agent file and behavior are implemented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaohuiing/skills/educlaw-agents)
- [Artifact skill overview](artifact/SKILL.md)
- [Artifact README](artifact/README.md)
- [Router configuration](artifact/router/config.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Conversational tutor responses with OpenClaw YAML configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The packaged subject agents declare no executable tools.]

## Skill Version(s):

2.0.1 (source: server release metadata and target metadata; artifact README has an older v0.1.0 test footer)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
