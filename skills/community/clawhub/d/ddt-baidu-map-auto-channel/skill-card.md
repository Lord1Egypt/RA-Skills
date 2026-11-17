## Description:

This skill analyzes automotive aftermarket channel coverage, brand scale, service types, and competitive context from Baidu Maps address text using published Diandiantong store snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External market and channel-planning users use this skill to evaluate chain automotive aftermarket brands, compare regional coverage and service-type distribution, and assess nearby store or site context from valid coordinates or public store IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An existing DDT_OPEN_BASE environment value could route requests and the API key to an unintended server.

Mitigation: Install only in a controlled shell environment, clear or explicitly set DDT_OPEN_BASE to https://gotoshop-ai.com/ddtclaw before using a real DDT_API_KEY, and rotate the key if it may have been used with an unexpected endpoint.

Risk: Coverage gaps or truncated preview results could lead to incomplete or overconfident market conclusions.

Mitigation: Check ok, coverage fields, and preview.truncated before concluding; label unavailable coverage clearly and narrow location queries instead of expanding automatically.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-baidu-map-auto-channel)
- [Skill homepage](https://gotoshop-ai.com/ddtclaw/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise analysis, key metrics, coverage notes, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should avoid API keys, internal fields, storage IDs, supplier fields, and unsupported metrics.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
