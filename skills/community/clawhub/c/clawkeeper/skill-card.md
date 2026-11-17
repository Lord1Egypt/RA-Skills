## Description:

Tasks and habits that live in a plain markdown file on your machine. Free, private, and claw-native.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tallhamn](https://clawhub.ai/user/tallhamn)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to manage tasks, habits, notes, and periodic check-ins through the ClawKeeper CLI while keeping data in a local markdown-backed directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and relies on the npm `clawkeeper` package.

Mitigation: Install only when the package source and version are trusted for the environment.

Risk: Task and habit data can be shared when multiple agents use the same CLAWKEEPER_DIR.

Mitigation: Use a private per-user or per-agent CLAWKEEPER_DIR unless shared task data is intentional.

Risk: Delete and edit commands can affect the wrong item when matched by text.

Mitigation: Prefer stable item IDs and confirm exact IDs before deleting or changing tasks, habits, or notes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tallhamn/skills/clawkeeper)
- [Publisher profile](https://clawhub.ai/user/tallhamn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate on local markdown data under CLAWKEEPER_DIR and return JSON success or error objects.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
