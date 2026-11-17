## Description:

LLM one-shot Q&A, summaries, and generation via SkillBoss API Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to send one-shot prompts for Q&A, summarization, JSON-style responses, and text generation through SkillBoss API Hub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and included text are sent to SkillBoss's external LLM API.

Mitigation: Use this skill only when policy allows third-party processing, and avoid submitting secrets, confidential business data, personal data, or regulated content unless approved.

Risk: Use of the SkillBoss API requires an API key.

Mitigation: Use a scoped SkillBoss_API_KEY where possible and manage it as a secret.

## Reference(s):

- [SkillBoss API Hub Endpoint](https://api.SkillBoss.co/v1/pilot)
- [SkillBoss Setup Guide](https://SkillBoss.co/skill.md)
- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/skills/alvisdunlop-gemini)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SkillBoss_API_KEY and sends prompts to SkillBoss's external LLM API.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
