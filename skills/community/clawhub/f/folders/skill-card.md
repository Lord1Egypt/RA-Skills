## Description:

Index important directories and perform safe folder operations with proper security checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and other agent users use this skill to find, index, and reason about important local folders while applying path safety checks before folder operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Folder discovery can scan common locations under the user's home directory and maintain local path records.

Mitigation: Review proposed index additions before approving them and avoid storing sensitive or unnecessary paths.

Risk: Folder cleanup or trash operations can affect local workspaces, build outputs, or slow network drives.

Mitigation: Review cleanup proposals before execution, prefer OS trash over permanent deletion, and be cautious with network drives.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/folders)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with paths, proposed actions, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference a local folder index at ~/.config/folder-index.json and should ask before adding discovered folders or performing cleanup actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
