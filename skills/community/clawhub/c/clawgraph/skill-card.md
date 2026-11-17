## Description:

Automatically store explicit durable user facts and recall them later; do not infer or upgrade weak signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawgraphai](https://clawhub.ai/user/clawgraphai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use ClawGraph to persist explicitly stated durable facts about users, projects, teams, and preferences, then recall those facts in later conversations or workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to save stable personal, project, team, and preference facts persistently without requiring explicit per-fact opt-in.

Mitigation: Review the behavior before installation, disclose automatic memory use to affected users, and restrict storage to durable facts explicitly stated or confirmed in the current session.

Risk: Selected facts may be processed through the configured OpenAI-compatible provider and stored under ~/.clawgraph/data.

Mitigation: Use a dedicated revocable API key, confirm provider handling requirements, and establish a process to inspect, correct, and delete stored graph data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clawgraphai/skills/clawgraph)
- [ClawGraph Homepage](https://github.com/clawgraph/clawgraph)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python examples, plus JSON output from referenced CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the clawgraph CLI and OPENAI_API_KEY; stored graph data persists at ~/.clawgraph/data.]

## Skill Version(s):

0.1.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
