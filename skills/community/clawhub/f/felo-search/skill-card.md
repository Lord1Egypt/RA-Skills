## Description:

Felo Search lets an agent call Felo AI for real-time web search and AI-generated answers to questions that need current information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999)

### License/Terms of Use:


## Use Case:

Developers and Claude Code users use this skill to answer current-information queries such as news, weather, prices, documentation updates, travel, and recommendations. The skill sends the user's query to Felo and returns a concise Markdown answer with query analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can over-trigger on ordinary questions and send prompt text to a third-party API.

Mitigation: Use it only when live web search is intended, and avoid sending secrets, private code, personal data, or confidential business context.

Risk: The skill requires a Felo API key and includes command examples that may expose secrets if copied into logs or shell history.

Mitigation: Keep FELO_API_KEY in a secure environment configuration and avoid printing API keys during setup or troubleshooting.

Risk: The artifact uses fixed /tmp JSON examples for request construction.

Mitigation: Prefer safer temporary-file handling or direct JSON construction that avoids collisions and stale request data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangzhiming1999/skills/felo-search)
- [Felo AI](https://felo.ai)
- [Felo Open Platform Documentation](https://openapi.felo.ai/docs)
- [Felo Open Platform](https://openapi.felo.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown answer text with query-analysis details and inline shell commands for setup or execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FELO_API_KEY and sends user queries to the Felo API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
