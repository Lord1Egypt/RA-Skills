## Description:

This skill helps an agent query China customs intellectual property record status for brands and summarize filing records with logistics-oriented risk guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linhongbijkm-dot](https://clawhub.ai/user/linhongbijkm-dot)

### License/Terms of Use:

MIT-0

## Use Case:

External users, logistics teams, and compliance reviewers use this skill to check whether brands appear in customs intellectual property protection records and to decide whether shipment authorization or additional review is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates a WAF-protected customs lookup site.

Mitigation: Run it only when authorized to automate the site, and confirm that the workflow complies with applicable access rules.

Risk: The skill can install unpinned Python packages at runtime and fall back to an alternate package mirror.

Mitigation: Use an isolated, least-privileged environment, pin dependencies before deployment, and disable automatic mirror fallback where supply-chain controls require it.

Risk: Queries use plaintext HTTP and results are cached in a workspace CSV file.

Mitigation: Avoid submitting sensitive brand or shipment context through the tool, protect the workspace cache, and clear cached records when retention is not needed.

Risk: The skill provides logistics risk guidance that may affect shipping decisions.

Mitigation: Validate important results through an official trusted source before relying on them for shipment authorization or compliance decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linhongbijkm-dot/skills/customs-ip-search)
- [China customs intellectual property record search system](http://202.127.48.145:8888/zscq/search/jsp/vBrandSearchIndex.jsp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with JSON-backed query results and risk guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include per-brand record tables, source indicators, filing status, date ranges, and logistics recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
