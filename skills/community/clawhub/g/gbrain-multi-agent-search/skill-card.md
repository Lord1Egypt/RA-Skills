## Description:

Search and manage a local gbrain personal knowledge base with full-text search, semantic search, and knowledge graph commands for notes, emails, documents, diary entries, and other stored knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[my12121-beep](https://clawhub.ai/user/my12121-beep)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure and run gbrain CLI workflows for querying a local personal knowledge base, reading matched pages, traversing graph links, and syncing or embedding markdown content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive personal notes, emails, documents, and diary entries in a local gbrain or brain repository.

Mitigation: Install only for agents authorized to inspect that repository and limit repository access to the content needed for the task.

Risk: Embedding workflows may send private material to a remote OpenAI-compatible endpoint.

Mitigation: Use a local or self-hosted embedding backend for private material when possible and configure any remote endpoint deliberately.

Risk: Sync, embed, link, and related data-management commands can mutate the brain repository or knowledge graph.

Mitigation: Require explicit confirmation before running sync, embed, link, or other mutation commands.

Risk: Persistent setup examples include an OPENAI_API_KEY variable.

Mitigation: Avoid storing real API keys in persistent instruction files; provide credentials through controlled environment or secret-management mechanisms.

## Reference(s):

- [gbrain GitHub repository](https://github.com/nicepkg/gbrain)
- [ClawHub skill page](https://clawhub.ai/my12121-beep/skills/gbrain-multi-agent-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command-oriented guidance for an agent to run local gbrain search, graph, sync, embed, statistics, and health-check workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
