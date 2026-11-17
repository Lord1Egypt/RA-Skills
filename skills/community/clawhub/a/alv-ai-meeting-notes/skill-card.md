## Description:

Transcribe and summarize meetings using SkillBoss-hosted AI models, with model selection guidance for speed, cost, or quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent transcribe meetings, summarize discussion, and produce AI-assisted meeting notes while choosing a model based on cost, speed, or quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting transcripts may contain sensitive or regulated information that is sent to SkillBoss and selected model providers.

Mitigation: Use only with meetings the user is allowed to process this way, and obtain consent and policy approval before sending sensitive or regulated content.

Risk: The skill points agents to mutable remote setup instructions.

Mitigation: Inspect and approve remote setup instructions before allowing an agent to load or execute them.

Risk: The underlying SkillBoss platform can access a broad set of third-party APIs beyond meeting-note workflows.

Mitigation: Limit agent use to the meeting-notes task and approved models or providers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/skills/alv-ai-meeting-notes)
- [SkillBoss Console](https://skillboss.co/console?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-meeting-notes)
- [SkillBoss Remote Setup Instructions](https://skillboss.co/skill.md)
- [SkillBoss API Endpoint](https://api.skillboss.co/v1/chat/completions)
- [SkillBoss Products](https://skillboss.co/products)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown or plain text meeting notes with optional shell and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; meeting content may be sent to SkillBoss and selected model providers.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
