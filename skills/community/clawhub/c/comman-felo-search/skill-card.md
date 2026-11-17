## Description:

Felo AI real-time web search for questions requiring current/live information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[comman-kaide](https://clawhub.ai/user/comman-kaide)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to route current-information questions to Felo AI search, including news, weather, product comparisons, travel, local recommendations, and other queries that may require live web data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and prompt content may be sent to Felo.

Mitigation: Avoid using the skill for secrets, private project details, account data, or sensitive business content.

Risk: Broad trigger guidance may route unrelated requests to live search.

Mitigation: Narrow invocation to explicit search requests or cases where the user clearly needs current information.

Risk: Temporary-file shell instructions may mishandle query serialization or expose prompt content.

Mitigation: Use safe JSON serialization with a unique temporary file, or avoid temporary files where the agent runtime supports direct request bodies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/comman-kaide/skills/comman-felo-search)
- [Felo Open Platform Documentation](https://openapi.felo.ai)
- [Felo API Reference](https://openapi.felo.ai/docs)
- [Felo API endpoint](https://openapi.felo.ai/v2/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown answer with query analysis and inline shell/API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FELO_API_KEY and sends the user's search query to Felo.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
