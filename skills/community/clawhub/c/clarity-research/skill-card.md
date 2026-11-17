## Description:

Search protein folding research data from Clarity Protocol by disease or protein name, list variants, and get API information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarityprotocol](https://clawhub.ai/user/clarityprotocol)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and analysts use this skill to query Clarity Protocol protein mutation and fold-result data, including disease-specific variants, protein-specific variants, UniProt IDs, and AlphaFold confidence scores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requests to clarityprotocol.io and may include CLARITY_API_KEY in an X-API-Key header when configured.

Mitigation: Install only when outbound HTTPS requests to Clarity Protocol are acceptable, and provide CLARITY_API_KEY only when higher rate limits are needed.

Risk: Anonymous use is rate limited and API responses may fail, time out, or return paginated results.

Mitigation: Use the documented API key option for higher limits, review command output for error messages, and account for pagination when using returned data.

## Reference(s):

- [Clarity Protocol](https://clarityprotocol.io)
- [Clarity Protocol API](https://clarityprotocol.io/api/v1)
- [Clarity Research on ClawHub](https://clawhub.ai/clarityprotocol/skills/clarity-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON or summary command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make HTTPS GET requests to clarityprotocol.io and may send CLARITY_API_KEY as an X-API-Key header when the environment variable is set.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
