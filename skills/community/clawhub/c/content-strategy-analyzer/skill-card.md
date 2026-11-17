## Description:

Analyzes websites to generate multi-language content strategy, keyword research, and competitor analysis for country- and language-specific content marketing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanzt](https://clawhub.ai/user/yanzt)

### License/Terms of Use:


## Use Case:

External marketers, content strategists, and developers use this skill to analyze a target website, identify localized competitors and keywords, and produce a three-month content plan for a selected country, language, and publishing cadence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler can fetch arbitrary URLs, including locations that may expose internal networks or cloud metadata endpoints.

Mitigation: Run it only on trusted public URLs and add private-network, metadata-address, and redirect blocking before use in sensitive environments.

Risk: Generated Excel files may contain formula-like values derived from untrusted analysis input.

Mitigation: Sanitize cell values before workbook generation so untrusted strings cannot be interpreted as formulas.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanzt/skills/content-strategy-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report, JSON website crawl data, and Excel workbook]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow asks for a target URL, country, language, and publishing frequency, then can generate website_data.json and content_plan.xlsx.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
