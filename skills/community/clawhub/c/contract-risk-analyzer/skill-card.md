## Description: <br>
Contract Risk Analyzer reviews uploaded contract PDFs, extracts key terms, and produces a structured AI-assisted risk report with severity-ranked findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiji0802](https://clawhub.ai/user/qiji0802) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, procurement teams, HR teams, freelancers, and small businesses use this skill to triage Chinese or English contract PDFs before legal review. It extracts text, detects contract type, identifies key terms, grades risks, and returns an informational report that is not legal advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded contracts and extracted text may contain confidential or regulated information. <br>
Mitigation: Process only contracts that are approved for the configured AI provider and delete /tmp/contracts outputs after use for confidential documents. <br>
Risk: The workflow requires API credentials and may use paid-tier tokens. <br>
Mitigation: Use a dedicated low-privilege API key and provide a paid-tier token only when needed. <br>
Risk: The report is AI-assisted and may miss or misstate legal risks. <br>
Mitigation: Treat the output as informational triage and have a qualified legal professional review contract decisions. <br>
Risk: The tool stores report files and optional CSV exports under /tmp/contracts. <br>
Mitigation: Confirm the exact PDF before analysis and remove generated reports and CSV files after delivery. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qiji0802/contract-risk-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/qiji0802) <br>
- [Commercial tier information](https://yk-global.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report, JSON command output, and optional CSV export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports summarize contract content, key terms, risk findings, severity levels, recommendations, extraction statistics, and optional CSV rows for paid tiers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
