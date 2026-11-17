## Description:

Autonomy Gate helps an AI agent check its operating authority level before external actions and supports level-change reviews and weekly self-assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to define and check an agent's allowed autonomy level before external actions such as messages, posts, email, deployment, service monitoring, or shutdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may influence or update its own authorization state.

Mitigation: Keep privilege increases and state changes operator-approved and enforce them outside the skill text.

Risk: Approved external channels or templates may be too broad or stale.

Mitigation: Validate approved channels and templates before use and keep placeholders or test values out of production configuration.

Risk: Emergency service shutdown authority may disrupt operations if applied autonomously.

Mitigation: Remove autonomous shutdown authority or tightly scope it to pre-approved services and explicit operator policy.

## Reference(s):

- [Autonomy Gate state reference](references/state.json)
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/skills/autonomy-gate)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Text]

**Output Format:** [Markdown guidance with JSON state references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses references/state.json as the current authority-state reference; no code execution or API calls are included in the artifact.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
