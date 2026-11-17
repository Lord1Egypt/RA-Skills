## Description:

Track macro variables such as VIX, US10Y, DXY, gold, oil, and BTC, returning current values, changes, and AI-generated impact analysis linked to the user's holdings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to track macro indicators, fetch a current macro dashboard, and understand how macro changes may affect portfolio holdings. It supports adding, removing, listing, and interpreting tracked indicators through AlphaGBM API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to AlphaGBM using an API key and may return analysis tied to portfolio or profile data.

Mitigation: Use a tightly scoped ALPHAGBM_API_KEY and avoid exposing portfolio-linked outputs beyond the intended agent session.

Risk: ALPHAGBM_BASE_URL can override the default service destination.

Mitigation: Keep ALPHAGBM_BASE_URL pointed only at the official AlphaGBM service unless a trusted deployment is explicitly required.

Risk: Broad natural-language triggers can add or remove tracked indicators when the user's request is ambiguous.

Mitigation: Confirm add, remove, and portfolio-linked lookup actions before calling the API when the prompt is unclear.

## Reference(s):

- [AlphaGBM website](https://alphagbm.com)
- [AlphaGBM service endpoint](https://alphagbm.zeabur.app)
- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-macro-view)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown with API request details, tables, and concise portfolio impact summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include current and previous indicator values, percent changes, supported indicator catalogs, and stale-data notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
