## Description:

Provides a quantitative yes/no evaluation framework for agent performance with scoring rules, scheduled self-review, and feedback loops for continuous improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luaqnyin](https://clawhub.ai/user/luaqnyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to define measurable evaluation checklists across content, legal, research, literature, analysis, and medical agents, score task outputs, and trigger improvement actions from recurring reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic workflow can read broad task-history memory and write persistent agent-memory records without clear user control.

Mitigation: Use sanitized task summaries, require explicit approval before SOUL.md or model/config inspection, and review persistent pattern or PAT updates before they are saved.

## Reference(s):

- [Agent Eval on ClawHub](https://clawhub.ai/luaqnyin/skills/agent-eval)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown checklists, scoring rubrics, workflow schedules, and record templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes weighted yes/no criteria, score tiers, recurring review triggers, and persistent evaluation record formats.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
