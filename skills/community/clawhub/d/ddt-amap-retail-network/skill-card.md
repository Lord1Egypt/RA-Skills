## Description:

Analyzes published DDT retail-store snapshots from Gaode Map address text to summarize brand scale, category mix, regional coverage, competitive context, and candidate-site opportunities while clarifying it is not an official Gaode Map product.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External retail analysts, site-selection teams, and business users use this skill to analyze published retail brand store networks from Gaode Map address text, including scale, category mix, regional coverage, city rankings, surroundings, and candidate-site screening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or request data could be sent to an unintended service if DDT_OPEN_BASE is overridden.

Mitigation: Set DDT_API_KEY only in a trusted environment, leave DDT_OPEN_BASE unset unless a custom endpoint is required, and verify the endpoint is the expected HTTPS DDT API service before use.

Risk: Retail conclusions can be misleading when API coverage is incomplete, a preview is truncated, or a brand is not published.

Mitigation: Check ok, coverage fields, data version, and preview.truncated before reporting conclusions; label unavailable coverage clearly and do not infer missing metrics.

Risk: Published snapshot data may not reflect store openings, closures, monthly changes, or actual site performance.

Mitigation: Present results as snapshot-based analysis, include coverage and data-version context, and avoid claims about business changes or site success probability unless the API response supports them.

## Reference(s):

- [DDT API Homepage](https://gotoshop-ai.com/ddtclaw/)
- [ClawHub Skill Page](https://clawhub.ai/horacetu/skills/ddt-amap-retail-network)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with concise retail conclusions, key metrics, coverage notes, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses only published snapshot data returned by the DDT API; avoids API keys, internal identifiers, supplier fields, unsupported metrics, and raw English enum fields.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
