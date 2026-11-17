## Description:

Control desktop applications with screen capture, OCR, mouse and keyboard automation, and reusable demonstration-taught tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power users use this skill to let an agent inspect the desktop, manipulate applications, and record or replay reusable workflow automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad access to screen contents and mouse and keyboard control.

Mitigation: Install only when this level of desktop access is intentional, and avoid use around passwords, banking, admin prompts, private messages, or sensitive documents.

Risk: Saved desktop tasks can replay actions with weak safeguards.

Mitigation: Review learned task files before running them, and treat task names and task JSON as trusted inputs only.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fuzzyb33s/skills/desktop-agent)
- [Skill usage documentation](artifact/skill.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, files, guidance]

**Output Format:** [Markdown with Python examples, CLI commands, task JSON, screenshots, and plain-text execution results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create screenshot image files and saved learned-task JSON files in the configured workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
