## Description: <br>
Generates professional consulting-style reports from uploaded PPT, text, PDF, image, and other source materials, with adaptive structure, research augmentation, and PPT, DOCX, PDF, or mind-map PDF outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericshao2025](https://clawhub.ai/user/ericshao2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, consultants, and analysts use this skill to turn project, manufacturing, market, technical, or business materials into structured professional reports and presentation-ready deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect uploaded documents and persist extracted content or logs. <br>
Mitigation: Use it only with documents approved for the environment, and review or clear generated extraction and log files when handling sensitive material. <br>
Risk: The skill can perform web research, use a local model endpoint, and send finished reports to external channels. <br>
Mitigation: Disable web search, local model calls, and automatic delivery for sensitive documents unless each action and destination is explicitly approved. <br>
Risk: The skill can scan installed local skills and rewrite its own skill files through self-evolution or self-repair behavior. <br>
Mitigation: Disable self-evolution, self-repair, and local skill scanning unless change review is planned; inspect any proposed file changes before reuse. <br>
Risk: Server security evidence marks this release as suspicious and recommends review before installation. <br>
Mitigation: Install only in a controlled environment after reviewing the release, its generated files, and its security scan results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericshao2025/consulting-report-generator) <br>
- [requirements-summary.md](references/requirements-summary.md) <br>
- [report-templates.md](references/report-templates.md) <br>
- [consulting-phrases.md](references/consulting-phrases.md) <br>
- [generate_pro.py](references/generate_pro.py) <br>
- [generate_docx.py](references/generate_docx.py) <br>
- [generate_pdf.py](references/generate_pdf.py) <br>
- [generate_mindmap.py](references/generate_mindmap.py) <br>
- [generate_offline_content.py](references/generate_offline_content.py) <br>
- [extract_content.py](references/extract_content.py) <br>
- [deep_research.py](references/deep_research.py) <br>
- [self_evolution.py](references/self_evolution.py) <br>
- [self_repair.py](references/self_repair.py) <br>
- [repair_pptx.py](references/repair_pptx.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance plus generated report files such as PPTX, DOCX, PDF, or mind-map PDF.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is PPT; DOCX, PDF, and mind-map PDF are selected through user instructions.] <br>

## Skill Version(s): <br>
6.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
