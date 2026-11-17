## Description:

Master the art of spawning and managing sub-agents. Write prompts that actually work, track running agents, and learn from every outcome.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to design structured prompts, coordinate sub-agent work, track active agents, and capture lessons from agent outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes sending selected prompt content to a third-party LLM endpoint.

Mitigation: Use the SkillBoss API portion only with approved data, and avoid sending secrets, proprietary code, credentials, personal data, or broad conversation context.

Risk: The skill recommends persistent local tracking notes for agent activity and learnings.

Mitigation: Configure tracking files deliberately so operational notes do not pollute repositories or persist sensitive workspace details unintentionally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeltennyson/skills/agent-orchestration1)
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with prompt templates, tracking-table examples, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SKILLBOSS_API_KEY when applying the optional SkillBoss API Hub example.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
