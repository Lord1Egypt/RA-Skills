## Description:

LLM one-shot Q&A, summaries, and generation via SkillBoss API Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route one-shot questions, summaries, and text generation requests through SkillBoss API Hub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and supplied text are sent to SkillBoss and may be routed to model providers.

Mitigation: Avoid submitting secrets, private customer data, regulated records, or proprietary material unless the organization has approved that data flow.

Risk: Generated answers, summaries, or JSON may be inaccurate or incomplete.

Mitigation: Review generated content before relying on it in customer-facing, regulated, or operational workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/alvis2-gemini)
- [SkillBoss pilot API endpoint](https://api.SkillBoss.co/v1/pilot)
- [SkillBoss setup guide](https://SkillBoss.co/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SkillBoss_API_KEY and sends prompts to SkillBoss API Hub.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
