## Description:

Upload files to lmfiles.com and return public download links via API for CLI-based file hosting, quick share links, bot-accessible file upload, account registration, file metadata lookup, file listing, and deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[setdemos](https://clawhub.ai/user/setdemos)

### License/Terms of Use:


## Use Case:

Developers, operators, and agents use this skill to register with lmfiles.com, upload files through its API, retrieve public download links and metadata, list account files, and delete uploaded files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded files are available to anyone with the returned public link.

Mitigation: Confirm the file is safe to publish and avoid uploading secrets, credentials, or private data.

Risk: API keys and bootstrap tokens can grant account or registration access if exposed.

Mitigation: Store credentials in environment variables, avoid logging or pasting them, and rotate bootstrap tokens if exposure is suspected.

Risk: The delete helper deletes the requested file_id without a dry run or confirmation prompt.

Mitigation: Verify the target file_id before running deletion commands.

## Reference(s):

- [LMfiles service documentation](https://lmfiles.com/docs)
- [LMfiles OpenAPI schema](https://lmfiles.com/openapi.json)
- [LMfiles API host](https://lmfiles.com)
- [ClawHub skill page](https://clawhub.ai/setdemos/skills/filehost)
- [Publisher profile](https://clawhub.ai/user/setdemos)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads return public download links; authenticated operations require LMFILES_API_KEY.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
