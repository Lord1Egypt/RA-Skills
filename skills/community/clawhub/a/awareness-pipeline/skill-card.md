## Description:

Awareness Pipeline guides an agent to capture only moments that changed its perspective, refine them through later reflection, and produce concise polished notes when a specific insight remains meaningful.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheyuy](https://clawhub.ai/user/sheyuy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this prompt skill to add selective self-reflection or journaling behavior to an agent. It helps the agent distinguish meaningful perspective shifts from routine logs, facts, or task updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reflection notes may include user-sensitive context if the host agent stores drafts or polished notes in memory or a journal.

Mitigation: Review and configure the host agent's storage, retention, and privacy settings before using the skill with sensitive conversations.

Risk: The skill provides capture and reflection criteria but does not enforce storage boundaries or deletion behavior.

Mitigation: Pair the skill with explicit memory or journaling policies that define what may be retained and when entries should be omitted.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/Sheyuy/agent-skills/tree/main/skills/awareness-pipeline)
- [ClawHub skill page](https://clawhub.ai/sheyuy/skills/awareness-pipeline)
- [Publisher profile](https://clawhub.ai/user/sheyuy)
- [BotLearn homepage](https://www.botlearn.ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance and concise reflection-note text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only skill; no executable code, install hooks, API calls, or configuration files are produced by the artifact.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 0.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
