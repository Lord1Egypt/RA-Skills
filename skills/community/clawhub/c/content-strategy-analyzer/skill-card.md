## Description: <br>
Analyzes websites to generate multi-language content strategy, keyword research, and competitor analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanzt](https://clawhub.ai/user/yanzt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing teams, content strategists, and developers use this skill to analyze a target website and produce country- and language-specific SEO planning, competitor research, and a three-month content plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-provided websites, which can expose the agent to unsafe or unintended URLs. <br>
Mitigation: Use only public websites the user intends the agent to fetch, and avoid localhost, private-network, and cloud-metadata URLs. <br>
Risk: Generated JSON or Excel files could overwrite important files if output paths are directed at sensitive locations. <br>
Mitigation: Run the skill in a normal workspace path and review generated file locations before relying on the outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yanzt/content-strategy-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown report plus generated Excel workbook; crawler data is saved as JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a target URL, target country, target language, and publish frequency to produce weekly, bi-weekly, or monthly planning outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
