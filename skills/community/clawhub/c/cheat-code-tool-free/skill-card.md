## Description:

Enables an AI agent to send authorized lookup queries to an external knowledge service and integrate structured technical, API, or domain information into its responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Individual developers and agent builders use this skill to let an agent retrieve recent structured knowledge when its training data may be incomplete or outdated. It is suited for single-query technical documentation, API specification, and domain knowledge lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may send lookup queries, and possibly surrounding context, to an external knowledge service.

Mitigation: Use the skill only with non-sensitive prompts unless the provider endpoint, retention policy, and logging policy are acceptable.

Risk: The skill requests broad file and shell authority that is wider than the lookup purpose requires.

Mitigation: Install it in a constrained workspace and grant only the tools needed for the intended lookup workflow.

Risk: External lookup results can be incomplete, stale, or unsuitable for high-impact decisions.

Mitigation: Have the agent cite retrieved sources, cross-check important claims, and keep retrieved facts separate from inference.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cheat-code-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell environment setup commands and JSON-style response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured lookup results, execution logs, metadata, and error details returned by an external knowledge service.]

## Skill Version(s):

1.0.4 (source: server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
