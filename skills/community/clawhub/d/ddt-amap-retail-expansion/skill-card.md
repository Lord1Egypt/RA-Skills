## Description:

Analyzes retail chain expansion opportunities, candidate-address competition, and rollout order from Amap-copied place and address text using DDT published retail store snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External retail expansion teams and site-selection analysts use this skill to evaluate published retail brands, compare regional coverage, inspect candidate-site competition, and produce verifiable next-step analysis from DDT store snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented DDT_OPEN_BASE environment variable can redirect bearer-token API requests to an inherited or untrusted API origin.

Mitigation: Use the skill only in controlled environments where DDT_OPEN_BASE cannot be set by untrusted code, or require the official API origin to be hardcoded or strictly validated before sending DDT_API_KEY.

Risk: Site-screen and nearby-store outputs are limited previews and may not represent a complete market inventory or forecast opening success.

Mitigation: Present these outputs as initial screening evidence and require local verification, coverage checks, and additional business review before acting on expansion decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-amap-retail-expansion)
- [DDT ClawHub homepage](https://gotoshop-ai.com/ddtclaw/)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration guidance]

**Output Format:** [Markdown with concise findings, key metrics, coverage notes, and limited store details when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DDT_API_KEY; uses published retail snapshots and should not expose API keys, internal identifiers, suppliers, or unsupported fields.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
