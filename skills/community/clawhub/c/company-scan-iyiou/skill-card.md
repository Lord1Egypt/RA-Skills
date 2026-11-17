## Description:

Company Scan helps agents search the IYIOU company database for businesses matching industry, geography, financing round, financing amount, and recency filters, then return a structured company list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-byte](https://clawhub.ai/user/ai-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to turn company-search requests into IYIOU query parameters, run the included Python search helper, and present matching companies with financing, location, industry, and link fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company-search terms are sent to IYIOU and result links point to IYIOU.

Mitigation: Install only when that data sharing and link destination are acceptable for the deployment.

Risk: The helper writes --output-temp results to a fixed shared filename in the system temp directory.

Mitigation: Use a securely created per-run temporary file or an explicit private output path before treating the skill as low risk.

Risk: The skill uses forceful routing and display wording that may over-trigger the skill or over-prescribe result handling.

Mitigation: Review and narrow invocation and display wording before broad deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ai-byte/skills/company-scan-iyiou)
- [IYIOU company data list](https://data.iyiou.com/company/comlist)
- [IYIOU company search API endpoint](https://api-open-data.iyiou.com/llm/company/search)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown company table, with optional JSON output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can be written to a temporary Markdown file when --output-temp is used; default max results is 50.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
