## Description: <br>
Family Soul analyzes family or group chat exports and generates a collective soul.md plus member persona Markdown files for use as AI agent persona foundations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zengury](https://clawhub.ai/user/zengury) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Family Soul to turn consented chat exports into Markdown persona material for agent grounding, including collective and per-member profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive chat exports and includes private-looking bundled chat or output data. <br>
Mitigation: Remove bundled chat/exported output data before distribution and run the skill only on records whose participants have consented to analysis. <br>
Risk: Conversation logs or derived personality profiles may be sent to cloud AI providers. <br>
Mitigation: Disclose the providers and data flow to participants, confirm consent, and review organizational privacy policy before processing logs. <br>
Risk: Hardcoded Kimi credentials are reported by the authoritative security guidance. <br>
Mitigation: Delete hardcoded credentials, rotate affected keys, and require runtime secrets through environment variables or a managed secret store. <br>
Risk: Parser behavior may process more data than the user-selected file. <br>
Mitigation: Fix or verify input scoping so the pipeline reads only the explicit file selected by the user before running on sensitive directories. <br>


## Reference(s): <br>
- [Family Soul ClawHub Release](https://clawhub.ai/zengury/family-soul) <br>
- [zengury ClawHub Publisher Profile](https://clawhub.ai/user/zengury) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, guidance] <br>
**Output Format:** [Markdown files with progress/status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces soul.md and member persona Markdown files; may emit agent-readable progress markers while running.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
