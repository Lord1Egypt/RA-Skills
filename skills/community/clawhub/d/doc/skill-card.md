## Description: <br>
Use when the task involves reading, creating, or editing `.docx` documents, especially when formatting or layout fidelity matters; prefer `python-docx` plus the bundled `scripts/render_docx.py` for visual checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flywhale-666](https://clawhub.ai/user/flywhale-666) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers, document automation users, and agents use this skill to read, create, edit, and visually review DOCX documents where formatting, tables, pagination, or layout fidelity matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package-manager or system-tool commands may install dependencies in the user's environment. <br>
Mitigation: Review installation commands before running them and approve them only when the source is trusted. <br>
Risk: Cleanup steps could remove files outside the intended workspace if applied too broadly. <br>
Mitigation: Keep cleanup limited to temporary or skill-owned paths such as `tmp/docs/` and generated document outputs. <br>
Risk: If rendering tools are unavailable, DOCX layout issues may be missed during text-only review. <br>
Mitigation: Use the visual render workflow when possible; if unavailable, disclose the layout risk and ask for local rendered review. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Files] <br>
**Output Format:** [Markdown guidance with shell commands and edited DOCX files when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May render DOCX pages to PNG for visual review and return updated documents plus a concise change summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
