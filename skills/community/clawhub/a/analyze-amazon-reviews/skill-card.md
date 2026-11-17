## Description:

Fetch Amazon product reviews through the Reveyes task API, choose cost-aware sampling by user intent, reuse permanent tasks, perform evidence-grounded Voice of Customer analysis, and generate a self-contained interactive HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuojiuya](https://clawhub.ai/user/zhuojiuya)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, product teams, listing operators, marketers, and support teams use this skill to analyze Amazon ASIN review samples for product health, pain points, return reasons, selling points, listing gaps, media defects, variants, and competitor comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential exposure or misuse of the Reveyes API key.

Mitigation: Read the key from REVEYES_API_KEY, an explicit env file, or hidden prompt only; do not paste it into prompts, reports, or source files, and rotate any key pasted into chat.

Risk: Review tasks and fetched results are retained by a third-party service.

Mitigation: Use the skill only when that data handling is acceptable for the product and marketplace being analyzed.

Risk: Local raw outputs can contain reviewer names, profile URLs, and other review identity data.

Mitigation: Keep output directories private and delete or redact raw artifacts before sharing anything other than the generated report.html.

Risk: A custom REVEYES_BASE_URL or --base-url can send API keys and review data to an unintended destination.

Mitigation: Use a custom base URL only when the destination is fully trusted.

Risk: Paid fetches can consume more points than intended if submitted without a clear limit.

Mitigation: Generate a plan first, show the estimated maximum points, and require --confirm-max-points before fetch execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuojiuya/skills/analyze-amazon-reviews)
- [Reveyes](https://www.reveyes.cn/)
- [Reveyes review API reference](artifact/references/reveyes-api.md)
- [Scenario routing and sampling plans](artifact/references/scenario-routing.md)
- [Evidence-grounded review analysis methodology](artifact/references/analysis-methodology.md)
- [Semantic analysis JSON contract](artifact/references/analysis-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, json, html]

**Output Format:** [Markdown guidance with shell commands, JSON analysis files, and a self-contained HTML report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Reveyes API key. New fetches may consume Reveyes points; the default HTML report omits API keys, task IDs, reviewer names, and profile URLs.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
