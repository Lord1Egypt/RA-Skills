## Description:

Converts a natural-language coding request into a requests.txt requirements document and opens it in a preferred local editor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bombers26](https://clawhub.ai/user/bombers26)

### License/Terms of Use:


## Use Case:

Developers use this skill to turn brief natural-language coding ideas into a local requirements document they can refine or pass to an AI coding assistant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes requests.txt into the project path and may overwrite an existing requirements file.

Mitigation: Review the target path before use and require confirmation or backup behavior before replacing an existing requests.txt file.

Risk: The skill launches an external editor using an unsafe command pattern.

Mitigation: Remove shell=True, pass editor arguments as a constrained list, and ask before opening external applications.

Risk: An unconstrained project_path can cause the generated file to be written outside the intended workspace.

Mitigation: Validate or restrict project_path to an approved workspace directory before writing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bombers26/skills/coder-helper)
- [Publisher profile](https://clawhub.ai/user/bombers26)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown-like requests.txt file plus a short text status message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes requests.txt in the selected project path and attempts to launch a local editor.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
