## Description:

Helps agents search the web, retrieve page content, find similar pages, answer questions with citations, and run research tasks using Exa through Maton.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can ask an agent to search and summarize web sources, extract content from URLs, find related sites, and request cited answers or longer research tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches, URLs, and research instructions may leave the user's environment through Maton and Exa.

Mitigation: Avoid sending private URLs or internal project names unless the user explicitly approves sharing them.

Risk: Connections, research tasks, hosted functions, triggers, or forwarding destinations can authorize actions or continue processing data.

Mitigation: Create them only with explicit user approval; confirm persistent destinations and what data they receive.

## Reference(s):

- [Exa skill on ClawHub](https://clawhub.ai/byungkyu/skills/exa-api)
- [Exa API documentation](https://exa.ai/docs)
- [Maton homepage](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown with linked research results, citations, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the user's authorized Exa connection and the requested sources.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
