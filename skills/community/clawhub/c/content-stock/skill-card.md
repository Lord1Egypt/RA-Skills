## Description:

Analyze themes/news for stock selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fonilye](https://clawhub.ai/user/fonilye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to send a keyword, news title, or report topic for stock-selection analysis with fast or deep analysis depth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the API key and user stock-analysis queries to an external service over unencrypted HTTP.

Mitigation: Use only after changing the endpoint to HTTPS with a trusted hostname, and use a scoped, rotatable EASYALPHA_API_KEY while avoiding sensitive research queries.

Risk: The release evidence reports malformed trailing NUL bytes in SKILL.md.

Mitigation: Remove the trailing NUL bytes from SKILL.md before publishing or installing the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fonilye/skills/content-stock)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Streaming text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EASYALPHA_API_KEY and Node.js; supports fast and deep analysis depth.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
