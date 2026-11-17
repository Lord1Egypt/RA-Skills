## Description:

Compares accident insurance policy documents by extracting policy details, scoring seven coverage and claims dimensions, and producing a visual comparison report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwbwin](https://clawhub.ai/user/wwbwin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and insurance shoppers use this skill to compare two or more accident insurance policies, understand coverage differences, and receive plain-language cautions before making a purchase decision. The generated comparison is informational and should be checked against the original insurance contract.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive insurance policy documents and may send insurer or product names to external searches.

Mitigation: Require explicit user confirmation before OCR, LLM extraction, or external searches, and minimize the policy data shared outside the local environment.

Risk: The skill may create a persistent local HTML report and open it automatically.

Mitigation: Ask before writing or opening reports, store them only where the user approves, and avoid auto-open behavior by default.

Risk: The report uses templated HTML and remote chart JavaScript.

Mitigation: Escape all report content before insertion and bundle or integrity-pin the chart library before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwbwin/skills/baodan-zhaoyaojing)
- [Publisher profile](https://clawhub.ai/user/wwbwin)
- [Policy JSON schema](references/schema.md)
- [Seven-dimension scoring rules](references/dimension_config.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON comparison data, and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a persistent local HTML report and may open it in a browser.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
