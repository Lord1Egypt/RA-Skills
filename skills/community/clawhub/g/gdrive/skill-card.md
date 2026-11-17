## Description:

Access Google Drive in a privacy-safe way by only working inside an allow-listed set of approved folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nasusuna](https://clawhub.ai/user/nasusuna)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to browse, search, read, and upload Google Drive files only within folders that have been explicitly approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The approved-folder boundary depends on the underlying Google Drive connector enforcing the allow-list.

Mitigation: Before installation, confirm the connector prevents access outside approved folders.

Risk: Approved folders are accessible to the agent for reading, searching, downloading, and upload when enabled.

Mitigation: Approve only intended folders and restrict upload permissions to folders where agent writes are expected.

Risk: Admin-only folder approval changes could expand the agent's accessible Drive scope.

Mitigation: Limit add and remove approval privileges to trusted administrators.

## Reference(s):

- [ClawHub gdrive skill page](https://clawhub.ai/nasusuna/skills/gdrive)
- [nasusuna publisher profile](https://clawhub.ai/user/nasusuna)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs and actions should remain within approved Google Drive folders and respect configured permissions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
