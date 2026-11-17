## Description:

AtroSnow File Management guides agents through elephant-guide backend file upload, download, display, cache promotion, and FileMedia module workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gerald-luo](https://clawhub.ai/user/gerald-luo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when implementing file upload, image or attachment display, FileMediaModule updates, and conversion of temporary uploads into persisted file records in the elephant-guide backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The final workflow section can point users toward the file-management batch endpoint for business saves, conflicting with the service-layer createFileMedia() guidance.

Mitigation: Use createFileMedia() from the business service layer when promoting temporary uploads into permanent records, and update the workflow text before operational use.

Risk: Uploaded files may contain sensitive data and can be temporarily stored before promotion to permanent records.

Mitigation: Upload sensitive files only when temporary storage and possible permanent retention are intended and covered by the application's data-handling requirements.

## Reference(s):

- [Source skill definition](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/gerald-luo/skills/atrosnow-file-management)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with Java, JavaScript, Vue, JSON, and HTTP endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; no hidden execution behavior was reported by server security evidence.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
