## Description:

Generates structured consulting-style reports from PPT, text, PDF, image, and other inputs, with adaptive templates and PPT, DOCX, PDF, or mind-map PDF outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericshao2025](https://clawhub.ai/user/ericshao2025)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external consultants, and developers use this skill to turn source material into professional reports for manufacturing, operations, project, market, technical, and general business scenarios. It is intended for workflows that need structured analysis, presentation-ready content, and optional document or mind-map outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic third-party delivery could expose report contents or source documents outside the user's environment.

Mitigation: Use only with non-confidential inputs unless external delivery is disabled, reviewed, and approved for the deployment.

Risk: Persistent logs and self-modification can retain sensitive context or change skill behavior over time.

Mitigation: Run in an isolated workspace, disable or review logging and self-repair write-back, and inspect generated changes before reuse.

Risk: The documented curl-to-sh installer path can install unpinned third-party software.

Mitigation: Use verified, pinned dependencies installed through controlled package management instead of piping remote installer scripts to a shell.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ericshao2025/skills/consulting-report-generator)
- [requirements-summary.md](references/requirements-summary.md)
- [report-templates.md](references/report-templates.md)
- [consulting-phrases.md](references/consulting-phrases.md)
- [extract_content.py](references/extract_content.py)
- [deep_research.py](references/deep_research.py)
- [generate_pro.py](references/generate_pro.py)
- [generate_docx.py](references/generate_docx.py)
- [generate_pdf.py](references/generate_pdf.py)
- [generate_mindmap.py](references/generate_mindmap.py)
- [generate_offline_content.py](references/generate_offline_content.py)
- [repair_pptx.py](references/repair_pptx.py)
- [self_repair.py](references/self_repair.py)
- [self_evolution.py](references/self_evolution.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated Python and shell-command snippets for creating PPT, DOCX, PDF, and mind-map PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local report files and supporting extracted-content or repair artifacts during agent execution.]

## Skill Version(s):

6.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
