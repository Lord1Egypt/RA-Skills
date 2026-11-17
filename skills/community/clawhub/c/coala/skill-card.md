## Description:

Coala Client helps agents explain and use the coala-client CLI for chat with OpenAI-compatible LLMs, MCP servers, CWL toolsets, and skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hubentu](https://clawhub.ai/user/hubentu)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to get concise operational guidance for initializing coala-client, configuring provider credentials, running chat or single-prompt sessions, and managing MCP servers, CWL toolsets, and skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote or zip-based MCP toolsets and skills can introduce untrusted behavior into coala-client workflows.

Mitigation: Import MCP toolsets and skills only from trusted sources, and review remote or zip content before loading it.

Risk: Previously imported MCP servers or skills can remain active through local coala-client configuration.

Mitigation: Remove unwanted entries from ~/.config/coala/ when they should no longer be available.

## Reference(s):

- [Coala Client skill page](https://clawhub.ai/hubentu/skills/coala)
- [coala-client homepage](https://github.com/coala-info/coala_client)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command examples, environment variable names, config paths, and MCP or skill management guidance.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
