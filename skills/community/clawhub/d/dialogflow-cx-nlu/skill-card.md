## Description:

Manage intents and entity types in Google Dialogflow CX via REST API for creating, updating, and managing natural language understanding components.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yash-kavaiya](https://clawhub.ai/user/yash-kavaiya)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect and manage Google Dialogflow CX NLU resources, including intents, training phrases, and entity types.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Create, update, import, and delete operations can change live Dialogflow CX agent behavior.

Mitigation: Use least-privilege Google credentials, verify project, location, agent, intent, and entity type names before execution, and test mutating commands against non-production agents first.

Risk: Incorrect training phrases or entity values can degrade NLU classification and parameter extraction.

Mitigation: Review proposed intent and entity changes before applying them and validate behavior in a staging Dialogflow CX agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yash-kavaiya/skills/dialogflow-cx-nlu)
- [Intents API Reference](references/intents.md)
- [Entity Types API Reference](references/entities.md)
- [Dialogflow CX v3beta1 API endpoint](https://dialogflow.googleapis.com/v3beta1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python CLI examples, and REST API snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live Google Dialogflow CX resource names, API responses, and command output.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
