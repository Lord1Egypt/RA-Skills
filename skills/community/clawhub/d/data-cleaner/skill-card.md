## Description: <br>
Clean and standardize multi-format data with AI-assisted field identification, deduplication, missing-value handling, format normalization, multi-source merge, quality reporting, and Feishu output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffersplind92](https://clawhub.ai/user/jeffersplind92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams and developers use this skill to clean messy spreadsheet, CSV, JSON, or pasted data, then export normalized datasets or reports. It is aimed at workflows such as CRM cleanup, order cleanup, bank statement reconciliation, roster cleanup, and multi-system data merge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dataset-derived content may be sent to AI providers during field identification, classification, smart fill, or report generation. <br>
Mitigation: Use only data you are authorized to share, prefer local-only runs without an AI key when possible, and require opt-in prompts or redaction before enabling AI features. <br>
Risk: Feishu Bitable and Feishu document outputs can disclose cleaned data or quality reports outside the local environment. <br>
Mitigation: Disable Feishu output unless the destination workspace, credentials, and sharing permissions are approved for the dataset. <br>
Risk: The artifact claims local processing, but the security summary identifies AI and Feishu integrations as potential external disclosure paths. <br>
Mitigation: Document the external paths clearly for users and review the skill before installing or running it on sensitive datasets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeffersplind92/data-cleaner) <br>
- [Publisher profile](https://clawhub.ai/user/jeffersplind92) <br>
- [MiniMax API](https://platform.minimax.chat/) <br>
- [DeepSeek API](https://platform.deepseek.com/) <br>
- [YK-Global](https://yk-global.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Python API examples, CLI commands, cleaned CSV or Excel files, Feishu Bitable output, and Feishu-compatible Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tier limits control row counts, source counts, smart fill, fuzzy matching, merging, AI classification, reporting, and Feishu output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
