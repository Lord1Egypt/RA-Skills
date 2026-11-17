## Description:

Provides Baidu hot-search topic monitoring prompts and a Python helper for returning ranked topic, search-count, category, and trend-report style outputs.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill as a Baidu hot-topics monitoring template for requesting ranked hot-search lists, keyword popularity checks, and trend summaries. Outputs should be treated as demonstration data unless the implementation is updated to fetch and label live Baidu sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises live Baidu trend monitoring while scanner evidence says the helper currently returns hardcoded mock results.

Mitigation: Treat outputs as demo or template material; update the implementation to fetch live data and clearly label freshness and source before relying on it for monitoring or business decisions.

Risk: Trend and popularity outputs can be mistaken for current public-interest signals.

Mitigation: Cross-check any generated trend report against authoritative Baidu sources and require human review before using it in external reporting or decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guohongbin-git/skills/baidu-hot-cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown-style text and JSON-style examples; the helper script can print formatted text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; current scanner evidence says the helper returns hardcoded mock results.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
