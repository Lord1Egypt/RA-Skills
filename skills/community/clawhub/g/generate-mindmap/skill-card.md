## Description: <br>
Generates interactive mind maps from text or summaries and exports them as HTML, PNG, JPG, SVG, PDF, or XMind files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FtoIS](https://clawhub.ai/user/FtoIS) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn source material or summaries into structured mind maps and export interactive or shareable files for review, presentation, or further editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install Pillow into the user's Python environment during PNG, JPG, or PDF export. <br>
Mitigation: Review before installing, use a virtual environment or preinstall Pillow through normal dependency management, and avoid auto-installation on shared, locked-down, or system Python environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FtoIS/generate-mindmap) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Generator script](artifact/generate_mindmap.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [JSON mind-map data and shell commands that generate HTML, PNG, JPG, SVG, PDF, or XMind files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3. Pillow is required for PNG, JPG, and PDF export and may be installed automatically by the script.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
