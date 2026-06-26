## Description: <br>
Axioma Guard Ultimate helps agents assess downloaded ClawHub skills for security signals, quality issues, and possible improvements using documented check, improve, and destroy workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to review downloaded ClawHub skills, run security and quality checks, and request improvements or destruction workflows when a skill is judged unsafe. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The destroy workflow can permanently delete a user-supplied skill path. <br>
Mitigation: Use it only after manual review, verify the exact target path, and keep a backup before running destroy.py with confirmation. <br>
Risk: The check and improve workflows rely on hard-coded local helper paths. <br>
Mitigation: Inspect those paths before trusting results, and prefer scan-only or manual review when the expected helpers are absent or unfamiliar. <br>
Risk: The artifact documents publish and elevated-operation patterns that may have side effects outside a local review. <br>
Mitigation: Avoid publish or elevated commands unless that action is explicitly intended and the command has been reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kofna3369/axiomata-guard-ultimate) <br>
- [Artifact README](README.md) <br>
- [Artifact skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may describe local checks, improvement steps, quarantine actions, and deletion workflows for a target skill.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
