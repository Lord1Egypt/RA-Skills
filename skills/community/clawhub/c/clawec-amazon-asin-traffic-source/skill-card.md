## Description:

Uses ClawEC to analyze Amazon ASIN traffic sources, including keyword flow, related traffic, traffic keywords, order keywords, and optional AI interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and ecommerce operators use this skill to request ASIN traffic-source analysis for a selected marketplace and month. It helps agents retrieve traffic channel distribution, traffic keywords, order keywords, and optional AI analysis from ClawEC.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends ASIN research parameters and a ClawEC API key to clawec.com.

Mitigation: Install only when ClawEC is the intended service, store the API key carefully, avoid shared logs, and review the third-party service terms for business-data handling.

Risk: Optional AI interpretation may be delayed, fail, or be unavailable while raw traffic-source data is still returned.

Mitigation: Poll for completion within the documented retry window and present the current status or raw data when interpretation does not complete.

## Reference(s):

- [ClawEC API](https://www.clawec.com/api)
- [ClawHub Skill Page](https://clawhub.ai/anyunzhong/skills/clawec-amazon-asin-traffic-source)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON responses with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include traffic-source summaries, keyword lists, order-keyword results, point usage details, and optional asynchronous AI interpretation status.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
