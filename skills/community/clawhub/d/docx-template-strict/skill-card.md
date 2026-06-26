## Description: <br>
Strictly fills DOCX templates by replacing placeholder tokens while preserving covers, headers, sections, styles, layout, and optional figures or references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lpq6](https://clawhub.ai/user/lpq6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, students, and report authors use this skill when they need an agent to fill a Word DOCX template without changing the original template layout. It is suited for papers, coursework, reports, and other documents that rely on explicit placeholder tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Template filling depends on exact placeholder tokens, so missing or split tokens can cause generation to fail or leave placeholders unreplaced. <br>
Mitigation: Use templates with continuous tokens such as {{TITLE_CN}} and review the generated DOCX before relying on it. <br>
Risk: The helper script reads local DOCX, JSON, and optional image paths supplied for the task. <br>
Mitigation: Run it only on trusted local files for the intended document and review command arguments before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lpq6/docx-template-strict) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown instructions with bash command examples; generated DOCX files when the helper script is run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JSON data and DOCX templates with explicit placeholder tokens; PDF export is outside the skill scope.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
