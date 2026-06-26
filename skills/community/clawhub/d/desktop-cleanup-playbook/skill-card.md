## Description: <br>
Generates review-first desktop cleanup plans, classification rules, phased schedules, and checklists from a desktop folder or file list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect a Desktop or chosen cleanup folder, classify files, and produce a reviewable cleanup plan before taking action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local helper reads filenames and limited text metadata from the folder selected by the user. <br>
Mitigation: Run it only on the Desktop or another folder intentionally chosen for cleanup, and avoid home, system, repository, or sensitive data directories. <br>
Risk: Cleanup suggestions could be mistaken for approved file operations. <br>
Mitigation: Review the generated report, risk notes, and confirmation checklist before moving, deleting, sharing, or otherwise acting on files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/desktop-cleanup-playbook) <br>
- [README](README.md) <br>
- [Cleanup specification](resources/spec.json) <br>
- [Output template](resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance, Shell commands] <br>
**Output Format:** [Markdown reports or JSON summaries with cleanup sections, risk notes, confirmation checklists, and optional dry-run command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only planning workflow; the Python helper uses the standard library and can write a report file or stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
