## Description:

A multi-agent deliberation hub with 3 core agents and extensible extended agents. Activates on explicit request, can suggest calling user workspace skills with consent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adelpro](https://clawhub.ai/user/adelpro)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to structure decision support, risk assessment, tone selection, and multi-perspective reasoning through named advisory agents. It can suggest delegation to workspace skills only with transparent opt-in behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegation to other workspace skills can broaden the scope of the response, especially for sensitive or high-impact tasks.

Mitigation: Review any proposed delegation and approve only the specific workspace skill needed for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adelpro/skills/council-of-wisdom-omni)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis with per-agent sections and delegation prompts when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include consulted-agent summaries, risk levels, tone recommendations, and explicit consent requests before workspace-skill delegation.]

## Skill Version(s):

1.4.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
