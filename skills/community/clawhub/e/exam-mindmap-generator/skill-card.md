## Description: <br>
Generates a printable static HTML review plan from knowledge_map.json, combining a knowledge structure map, weak-point alerts, and a study plan, then asks whether to generate practice questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhoucha833-lang](https://clawhub.ai/user/zhoucha833-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and exam-preparation users use this skill to turn an existing knowledge map into an HTML study dashboard with priorities, weak-point warnings, and a date-based review plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated browser-opened report embeds content from knowledge_map.json. <br>
Mitigation: Use the skill only with trusted knowledge_map.json files and review the generated HTML before opening or sharing it. <br>
Risk: The generated report can load ECharts from BootCDN. <br>
Mitigation: Open reports only where third-party CDN loading is acceptable, or replace the dependency with an approved local or vetted source before deployment. <br>
Risk: The date-based HTML output can overwrite an older report. <br>
Mitigation: Keep copies of reports that must be preserved or run the skill in an isolated workspace. <br>


## Reference(s): <br>
- [Design Specification](references/design-spec.md) <br>
- [Review Plan Generation Rules](references/node-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, guidance] <br>
**Output Format:** [Static HTML file plus a short text prompt] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes an exam-mindmap-YYYYMMDD.html report and may overwrite an older report with the same date-based name.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
