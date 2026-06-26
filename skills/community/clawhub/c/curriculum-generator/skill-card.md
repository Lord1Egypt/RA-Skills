## Description: <br>
Intelligent educational curriculum generation system with strict step enforcement and human escalation policies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tarasinghrajput](https://clawhub.ai/user/tarasinghrajput) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External educators, curriculum owners, and POD operators use this skill to gather requirements, design or assess educational curricula, find educational resource links, and generate draft Excel or CSV curriculum outputs for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory may retain student, teacher, or institutional details. <br>
Mitigation: Avoid entering personal student data, inspect the memory directory, and periodically delete retained memory when it is no longer needed. <br>
Risk: Shell-based educational resource searches have unclear privacy and control boundaries. <br>
Mitigation: Use a constrained search tool or disable shell-based searches in sensitive environments. <br>
Risk: Draft curriculum recommendations can affect students, teachers, or POD operations if treated as final. <br>
Mitigation: Require curriculum owner or POD leader review before operational use, especially when inputs are ambiguous or changes are high impact. <br>


## Reference(s): <br>
- [Curriculum Generator ClawHub page](https://clawhub.ai/tarasinghrajput/curriculum-generator) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, files] <br>
**Output Format:** [Markdown guidance with generated CSV or Excel files and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store memory, templates, and generated outputs under ~/.openclaw/skills/curriculum-generator/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
