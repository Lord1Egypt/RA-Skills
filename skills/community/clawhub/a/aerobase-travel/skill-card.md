## Description:

Jetlag-aware flight intelligence for AI travel agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kurosh87](https://clawhub.ai/user/kurosh87)

### License/Terms of Use:


## Use Case:

External travel agents and agent developers use this skill to search, score, and explain flights by jetlag impact, recovery time, airport facilities, route strategy, and travel deal value.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flight routes, dates, times, and search preferences are sent to the external Aerobase API.

Mitigation: Install only if the user trusts Aerobase and is comfortable sharing those travel details with its API.

Risk: The skill uses AEROBASE_API_KEY for authenticated API calls.

Mitigation: Treat the API key as a secret and avoid sharing terminal logs or command snippets that include it.

## Reference(s):

- [Aerobase API](https://aerobase.app/api)
- [Aerobase Travel on ClawHub](https://clawhub.ai/kurosh87/skills/aerobase-travel)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, API calls]

**Output Format:** [Markdown with inline bash code blocks and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AEROBASE_API_KEY for external Aerobase API requests.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
