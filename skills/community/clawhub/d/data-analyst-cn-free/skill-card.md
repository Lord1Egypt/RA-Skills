## Description: <br>
Helps agents provide Chinese-language basic data analysis guidance for CSV and Excel files, including data preview, cleaning, descriptive statistics, and simple visualization code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data analysts, product managers, operations staff, and developers can use this skill to ask an agent for basic dataset inspection, cleanup steps, descriptive statistics, and matplotlib visualization snippets for CSV or Excel data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read and process user-provided datasets that contain sensitive or private information. <br>
Mitigation: Use only datasets the agent is authorized to access and avoid sharing analysis outputs beyond the intended environment. <br>
Risk: The optional callback_url parameter can send results to an external destination. <br>
Mitigation: Use callback_url only with trusted destinations, and omit it when results contain sensitive data. <br>
Risk: Generated local Python-style analysis commands may be incorrect for a specific dataset. <br>
Mitigation: Review generated code and commands before execution, especially when changing files or processing large datasets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/data-analyst-cn-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code snippets] <br>
**Output Parameters:** [1D; input is required, options and callback_url are optional] <br>
**Other Properties Related to Output:** [Chinese-language data analysis guidance focused on CSV and Excel data, basic cleaning, descriptive statistics, and simple visualizations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
