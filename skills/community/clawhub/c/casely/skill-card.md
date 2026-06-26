## Description: <br>
Intelligent QA assistant that automates writing test cases from project documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JohnWayneeee](https://clawhub.ai/user/JohnWayneeee) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
QA engineers and software teams use Casely to parse requirement documents, learn test-case style from examples, generate atomic test cases, and export TestRail-ready Excel files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local QA documents and examples that may contain confidential requirements or customer data. <br>
Mitigation: Run it only on intended project folders and review source documents before processing. <br>
Risk: The skill can create files under projects/ and may modify repository Python dependency files during uv setup. <br>
Mitigation: Specify the intended project path when multiple projects exist and review dependency changes before accepting them. <br>
Risk: Generated style guides, test cases, and spreadsheets may be inaccurate or unsuitable for direct import into a test-management system. <br>
Mitigation: Inspect generated Markdown and Excel exports before using them in QA workflows. <br>


## Reference(s): <br>
- [Casely ClawHub page](https://clawhub.ai/JohnWayneeee/casely) <br>
- [Parser Usage Guide](references/parser_usage.md) <br>
- [Export Guide](references/export_guide.md) <br>
- [Test Style Analysis Methodology](references/style_analysis_prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, local project files, generated test-case Markdown, and Excel workbook exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local project directories, processed Markdown files, test plans, atomic test-case files, and .xlsx exports.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
