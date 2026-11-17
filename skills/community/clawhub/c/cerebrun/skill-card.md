## Description:

Cerebrun is an MCP client for retrieving layered personal context, searching and updating knowledge, and using a Cerebrun LLM gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niyoseris](https://clawhub.ai/user/niyoseris)

### License/Terms of Use:


## Use Case:

External developers and agents use Cerebrun to retrieve user preferences, project context, personal identity layers, knowledge-base entries, and conversation history. They can also update context, store knowledge, request vault access, or send LLM gateway messages when those actions are intended.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access personal context, stored knowledge, conversation history, Layer 2 data, and vault-adjacent data.

Mitigation: Install and use it only when Cerebrun is trusted with that data, and avoid sending secrets or retrieved private context unless explicitly intended.

Risk: The update_context and push_knowledge operations can change persistent remote data.

Mitigation: Review the target layer, content, category, and tags before invoking persistent write operations.

Risk: Passing an API key as a command-line argument can expose credentials through local shell history or process inspection.

Mitigation: Prefer the CEREBRUN_API_KEY environment variable over --api-key.

## Reference(s):

- [Cerebrun MCP API Reference](references/REFERENCES.md)
- [ClawHub Cerebrun skill page](https://clawhub.ai/niyoseris/skills/cerebrun)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON API responses]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Cerebrun API key; operations may read or change remote personal context, knowledge, conversation, and vault-adjacent data.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
