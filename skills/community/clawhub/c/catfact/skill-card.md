## Description:

Random cat facts and breed information from catfact.ninja (free, no API key).

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesethrose](https://clawhub.ai/user/thesethrose)

### License/Terms of Use:


## Use Case:

External users and developers use this skill when they want an agent to fetch public cat facts or cat breed information for lightweight responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause the agent to contact catfact.ninja with curl when cat facts or breed information are requested.

Mitigation: Use it only for the disclosed public cat fact and breed endpoints, and do not include credentials or local data in requests.

## Reference(s):

- [Cat Fact API Documentation](https://catfact.ninja)
- [ClawHub Skill Page](https://clawhub.ai/thesethrose/skills/catfact)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl to request public JSON responses from catfact.ninja; no API key is required.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
