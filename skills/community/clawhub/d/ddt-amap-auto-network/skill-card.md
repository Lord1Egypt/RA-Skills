## Description:

Analyzes automotive aftermarket brand store networks, regional coverage, and location profiles from Amap-style place/address text using published DiandianTong store snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts and operators use this skill to evaluate automotive aftermarket chain brands, compare regional store coverage, and summarize nearby or single-store evidence when users provide valid coordinates, public store IDs, or Amap-style address text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An inherited DDT_OPEN_BASE value could redirect bearer API key requests to an unintended origin.

Mitigation: Unset DDT_OPEN_BASE or set it exactly to https://gotoshop-ai.com/ddtclaw before use, and rotate any key that may have been used with an untrusted base URL.

Risk: The security scan verdict is suspicious because the documented curl examples rely on environment-provided API configuration.

Mitigation: Install only when the publisher is trusted, keep DDT_API_KEY out of chats, logs, and repositories, and verify the API origin before running requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-amap-auto-network)
- [Publisher profile](https://clawhub.ai/user/horacetu)
- [Skill homepage](https://gotoshop-ai.com/ddtclaw/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should summarize conclusions, key metrics, coverage and data-version notes, requested store details, and uncovered items without exposing API keys, storage IDs, suppliers, or internal fields.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
