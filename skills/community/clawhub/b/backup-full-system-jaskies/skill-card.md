## Description:

Backs up OpenClaw system data, configuration, memory, and selected local system files, then uploads the archive to cloud storage with rclone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaskies](https://clawhub.ai/user/jaskies)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare and run a full OpenClaw backup workflow, including dependency setup, rclone configuration, archive creation, and cloud upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The backup process can collect broad local and privileged system data, including user configuration, shell profiles, crontab, Tailscale, systemd files, and unrelated home-directory files.

Mitigation: Restrict collection to explicit OpenClaw paths and require separate approval for any user, network, service, or unrelated home-directory files.

Risk: The archive is uploaded to Google Drive without clear confirmation of the destination or encryption before upload.

Mitigation: Confirm the rclone remote and destination before running the upload, and encrypt the backup archive before it leaves the machine.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaskies/skills/backup-full-system-jaskies)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational guidance for creating compressed backup archives and uploading them with rclone.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
