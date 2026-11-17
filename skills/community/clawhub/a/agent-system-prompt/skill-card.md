## Description:

Design and generate system prompts for AI agents, assistants, and chatbots. Use when creating, writing, or improving a system prompt, persona, role definition, or operating instructions for any AI agent (assistant, coding, autonomous, research, support, or orchestrator). Provides a component-based methodology, agent archetypes, and ready-to-fill templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent designers use this skill to turn requirements into clear system prompts for conversational, coding, autonomous, research, support, and orchestration agents. It guides them through choosing an archetype, assembling prompt components, adapting a template, and checking the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The autonomous-agent template contains guidance flagged as potentially bypassing safeguards and exposing a service beyond localhost.

Mitigation: Review and adapt the generated prompt; require confirmation for destructive or sensitive actions and keep development services limited to localhost.

## Reference(s):

- [Agent Archetypes](references/agent-types.md)
- [Prompt Components](references/anatomy.md)
- [Writing Patterns and Validation](references/output-patterns.md)
- [Autonomous Agent Template](assets/templates/autonomous-agent.md)
- [Conversational Assistant Template](assets/templates/chatbot.md)
- [Coding Agent Template](assets/templates/coding-agent.md)
- [Tool and API Orchestrator Template](assets/templates/orchestrator.md)
- [Research Agent Template](assets/templates/research-agent.md)
- [Customer Support Agent Template](assets/templates/support-agent.md)
- [ClawHub Skill Page](https://clawhub.ai/openlark/skills/agent-system-prompt)
- [Publisher Profile](https://clawhub.ai/user/openlark)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown system prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tailored to the selected agent archetype and the user's requirements.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
