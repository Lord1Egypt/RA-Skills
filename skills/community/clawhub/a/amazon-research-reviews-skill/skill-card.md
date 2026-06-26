## Description: <br>
AI-powered e-commerce review analysis skill that labels product reviews across 22 dimensions, identifies user personas and Voice of Customer insights, and generates CSV, Markdown, and HTML reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangdabiao](https://clawhub.ai/user/liangdabiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product, marketplace, and e-commerce teams use this skill to analyze customer review files, surface product pain points and opportunities, and create review intelligence outputs for product optimization, competitor analysis, market research, and user insight work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install the openpyxl Python package when Excel support is needed. <br>
Mitigation: Review before installing and preinstall a pinned openpyxl version in the execution environment if Excel processing is required. <br>
Risk: The skill creates local prompt, sample, intermediate, and output files that may contain copied review data. <br>
Mitigation: Use only intentionally selected review files, avoid sensitive or personal data unless local copies are acceptable, and inspect or delete generated files before sharing or committing the workspace. <br>
Risk: Generated review insights and recommendations may be incomplete or misleading if treated as final business guidance. <br>
Mitigation: Review generated CSV, Markdown, and HTML outputs before using them for product, market, or competitive decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liangdabiao/amazon-research-reviews-skill) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [CSV files, Markdown reports, HTML dashboard files, JSON intermediates, and shell-command-oriented workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes selected review files in batches of up to 30 reviews and writes generated analysis artifacts to local output directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
