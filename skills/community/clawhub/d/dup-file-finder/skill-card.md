## Description:

Quickly identifies and lists duplicate files in a specified local directory to help users manage disk space.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scan a chosen local directory for duplicate files and review the duplicate paths before deciding what to remove.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool opens and hashes every file under the directory supplied by the user, which may include sensitive local files.

Mitigation: Point it only at directories whose contents you are comfortable reading locally, and review the printed duplicate list before taking any cleanup action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/skills/dup-file-finder)
- [Publisher profile](https://clawhub.ai/user/albionaiinc-del)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text duplicate-file listings with optional markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports SHA-256 hashes and local file paths for duplicate groups; it does not delete files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
