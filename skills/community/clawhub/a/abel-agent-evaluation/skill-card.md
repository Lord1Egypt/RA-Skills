## Description:

Testing and benchmarking LLM agents including behavioral testing, capability assessment, reliability metrics, and production monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quality engineers, and agent builders use this skill to design and run behavioral regression tests, capability assessments, adversarial tests, and reliability evaluations for LLM agents before production deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evaluation prompts, transcripts, model outputs, and test cases may be sent to the SkillBoss/HeyBossAI API.

Mitigation: Redact secrets and personal or regulated data before use, and avoid confidential evaluations unless the provider is approved for that data.

Risk: The skill routes evaluation chat messages to a fixed third-party API without clear privacy controls or user choice.

Mitigation: Review the provider relationship, endpoint behavior, and data handling requirements before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeltennyson/skills/abel-agent-evaluation)
- [Complete setup guide](https://skillboss.co/skill.md)
- [SkillBoss API endpoint](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require SKILLBOSS_API_KEY and may send evaluation prompts, transcripts, model outputs, and test cases to the SkillBoss/HeyBossAI API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
