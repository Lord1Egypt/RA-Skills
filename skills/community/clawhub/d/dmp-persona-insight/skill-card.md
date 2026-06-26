## Description: <br>
Analyzes DMP audience persona data, extracts multi-dimensional TGI-based features, and produces structured persona insight reports and presentation-ready recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mingri26](https://clawhub.ai/user/mingri26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketers, product teams, and developers use this skill to retrieve DMP insight-task data with AK/SK credentials, analyze persona dimensions, identify core audience features, and generate marketing, operations, product-positioning, and presentation outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires DMP credentials and may process audience-insight data. <br>
Mitigation: Configure DMP_AK and DMP_SK only through secure secret or environment mechanisms, do not paste credentials into chat, rotate any exposed keys, and prefer anonymized or aggregated datasets. <br>
Risk: Evidence security guidance reports unsafe transport handling and warns against using the bundled API client until TLS certificate verification is enabled. <br>
Mitigation: Enable TLS certificate verification before using the API client with live credentials or production audience data. <br>
Risk: Generated persona, marketing, and strategy recommendations can be incomplete or misleading if the source data or analysis assumptions are wrong. <br>
Mitigation: Review reports and presentation outputs against source data and business constraints before acting on recommendations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mingri26/dmp-persona-insight) <br>
- [Mingdata ability center](https://open.mingdata.com/ability-center) <br>
- [Quickstart guide](references/quickstart.md) <br>
- [Operation guide](references/operation-guide.md) <br>
- [Insight API integration guide](references/insight-integration.md) <br>
- [Analysis framework](references/analysis-framework.md) <br>
- [Feature extraction standard](references/FEATURE_EXTRACTION_STANDARD.md) <br>
- [PPT v4.2 usage guide](references/ppt-v4.2-usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown reports, PowerPoint files, JSON-like API data, Python code examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DMP_AK and DMP_SK credentials; outputs may include audience-insight data and marketing recommendations that should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub server release metadata; artifact frontmatter version: 9.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
