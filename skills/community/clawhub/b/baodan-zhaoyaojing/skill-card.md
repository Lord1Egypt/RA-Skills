## Description: <br>
保单照妖镜 compares accident insurance policy documents by extracting policy terms, scoring seven coverage dimensions, checking claim-reputation signals, and generating a visual comparison report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwbwin](https://clawhub.ai/user/wwbwin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Insurance shoppers, advisors, or reviewers use this skill to compare two or more accident insurance policies from images or PDFs, identify coverage gaps, and produce a readable report. It is designed for comparison support and should not be treated as final investment, legal, or insurance advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes insurance policy documents that may contain personal or sensitive policyholder information. <br>
Mitigation: Redact personal identifiers and unnecessary policyholder details before using the skill. <br>
Risk: Claim-reputation checks may trigger live searches against external social, complaint, or regulatory sites. <br>
Mitigation: Approve external searches explicitly and avoid sending sensitive policy contents to third-party services. <br>
Risk: Generated HTML reports may load third-party charting scripts and contain real policy data. <br>
Mitigation: Open generated reports only in a trusted local environment and avoid third-party scripts for reports containing sensitive data. <br>
Risk: OCR and LLM extraction can misread policy clauses, limits, exclusions, or low-confidence fields. <br>
Mitigation: Review extracted terms against the original insurance contract before relying on the comparison. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwbwin/baodan-zhaoyaojing) <br>
- [Publisher profile](https://clawhub.ai/user/wwbwin) <br>
- [Policy extraction schema](references/schema.md) <br>
- [Seven-dimension scoring rules](references/dimension_config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON policy structures, shell commands, and generated HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate a local HTML report using a bundled template and charting script; users should review extracted fields and low-confidence values.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
