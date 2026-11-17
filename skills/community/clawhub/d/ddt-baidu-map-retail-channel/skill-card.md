## Description:

Analyzes retail channel structure, city coverage, competitor differences, and market opportunities from Baidu Map address text and Diandiantong published retail-store snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts and business users use this skill to evaluate published retail brands, compare store networks, assess local competition, and narrow candidate sites using aggregate snapshots and limited public store previews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer API keys could be sent to an unintended endpoint if DDT_OPEN_BASE is inherited from an untrusted shell or automation context.

Mitigation: Set DDT_OPEN_BASE explicitly to https://gotoshop-ai.com/ddtclaw/ in a controlled environment before running any sample curl command, and avoid inherited environment values.

Risk: The skill requires DDT_API_KEY for API calls, so accidental disclosure in chat, logs, or version control would expose credentials.

Mitigation: Keep real API keys out of skill files, prompts, logs, and repositories; use local secret management or scoped runtime environment variables.

Risk: Retail conclusions depend on published snapshots and coverage fields, so unsupported or stale data could produce misleading business conclusions.

Mitigation: Report coverage and data-version information with conclusions, stop when coverage is insufficient, and label unavailable coverage as not covered rather than zero.

## Reference(s):

- [Diandiantong ClawHub API homepage](https://gotoshop-ai.com/ddtclaw/)
- [ClawHub skill listing](https://clawhub.ai/horacetu/skills/ddt-baidu-map-retail-channel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with concise conclusions, key metrics, coverage and data-version notes, and limited store previews when explicitly requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DDT_API_KEY and the official DDT_OPEN_BASE service origin; outputs must not expose API keys, internal identifiers, supplier fields, or unsupported metrics.]

## Skill Version(s):

1.0.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
