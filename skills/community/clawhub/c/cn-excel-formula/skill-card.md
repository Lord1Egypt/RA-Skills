## Description: <br>
Chinese Excel formula assistant that turns natural-language requests into Excel formulas and provides formula explanations, examples, troubleshooting, and optimization guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and spreadsheet developers use this skill to generate, explain, list, and troubleshoot Excel formulas from Chinese natural-language descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spreadsheet descriptions sent with optional AI-enhanced generation may contain confidential business data. <br>
Mitigation: Use the default local template mode for sensitive data; enable AI-enhanced generation only when the OpenAI account and data handling policy are approved. <br>
Risk: Generated formulas or diagnostics may not match a workbook's exact structure or spreadsheet locale. <br>
Mitigation: Review and test formulas on non-critical copies of spreadsheets before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-excel-formula) <br>
- [AISoBrand website](https://aisobrand.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style terminal text with Excel formulas, explanations, examples, and diagnostic guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default generation uses local template matching; optional AI-enhanced generation uses OpenAI when the dependency and OPENAI_API_KEY are configured.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
