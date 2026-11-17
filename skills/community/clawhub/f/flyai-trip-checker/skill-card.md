## Description:

行程体检员验证已有行程方案，并输出价格、路线、时间、遗漏事项、风险诊断和优化建议的体检报告，支持文字、截图和订单输入。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to review an existing itinerary, compare current flight and hotel data, identify route or timing problems, and produce a concise optimization report before travel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guidance includes disabling TLS certificate verification when searches fail.

Mitigation: Require secure connection checks by default and only use trusted network and certificate remediation steps before running travel searches.

Risk: The skill asks agents to install the latest global FlyAI CLI package and includes sudo-oriented recovery guidance.

Mitigation: Prefer pinned package versions, isolated environments, and explicit user approval before installing or upgrading command-line tools.

Risk: The skill can read and update persistent personal travel profiles.

Mitigation: Make profile access opt-in, disclose what is stored, and provide clear controls for editing or deleting saved preferences.

Risk: The skill may surface third-party booking links in reports.

Mitigation: Validate booking URLs, label third-party destinations clearly, and keep booking links optional in the final report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hello-ahang/skills/flyai-trip-checker)
- [Output template](artifact/reference/output-template.md)
- [Scoring rules](artifact/reference/scoring-rules.md)
- [User profile storage](artifact/reference/user-profile-storage.md)
- [Flight search reference](artifact/reference/references/search-flight.md)
- [Hotel search reference](artifact/reference/references/search-hotel.md)
- [POI search reference](artifact/reference/references/search-poi.md)
- [AI search reference](artifact/reference/references/ai-search.md)
- [Keyword search reference](artifact/reference/references/keyword-search.md)
- [Train search reference](artifact/reference/references/search-train.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown travel audit report with inline FlyAI CLI commands and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include itinerary scores, price comparisons, route and schedule findings, risk notes, optimization suggestions, and third-party booking links.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
