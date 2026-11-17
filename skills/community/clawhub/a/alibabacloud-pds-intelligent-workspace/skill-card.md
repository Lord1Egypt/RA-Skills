## Description:

Provides agent guidance for operating Alibaba Cloud PDS cloud-drive files and spaces, including search, upload, download, file management, sharing, content analysis, image operations, archive downloads, and installing or mounting the PDS mount app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent perform or explain Alibaba Cloud PDS file-space workflows through documented Aliyun CLI commands. It is intended for PDS file operations, cloud-drive content analysis, sharing, image workflows, archive downloads, and mountapp setup for local-disk access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and mount workflows can download or execute unverified software.

Mitigation: Review the skill before installation, avoid curl-to-bash or unverified package installs, and verify mountapp origin and integrity before use.

Risk: PDS workflows require cloud credentials and may expose sensitive access paths if secrets are handled inside the agent session.

Mitigation: Use narrowly scoped Alibaba Cloud/PDS credentials and configure secrets outside the agent session.

Risk: Mountapp can create persistent local background services for cloud-drive access.

Mitigation: Confirm startup persistence and service behavior with the user before enabling the local mount service.

Risk: The scanner summary flags anti-inspection instructions requiring review.

Mitigation: Treat the scanner verdict as requiring manual review before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-pds-intelligent-workspace)
- [PDS Cloud Drive Mount App Plugin](https://help.aliyun.com/zh/pds/drive-and-photo-service-ent/user-guide/mount-drives?spm=a2c4g.750001.0.i2)
- [Aliyun CLI Documentation](https://help.aliyun.com/zh/cli/)
- [Aliyun CLI Plugin Repository](https://github.com/aliyun/aliyun-cli)
- [Access Key Management](https://ram.console.aliyun.com/manage/ak)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [PDS Aliyun CLI Configuration Guide](references/config.md)
- [RAM Permission Requirements](references/ram-policies.md)
- [PDS File Management](references/file-management.md)
- [PDS File Search](references/search-file.md)
- [PDS File Download Guide](references/download-file.md)
- [PDS Upload Guide](references/upload-file.md)
- [File Sharing](references/share-link.md)
- [PDS Document and Audio/Video Analysis](references/multianalysis-file.md)
- [PDS Image Editing Guide](references/image-editing.md)
- [PDS Visual Similar Search Guide](references/visual-similar-search.md)
- [PDS Archive Download Guide](references/archive-download.md)
- [PDS Drive Guide](references/drive.md)
- [Resolve Between Cloud Path and file_id](references/resolve-path.md)
- [PDS Mount App Guide](references/mountapp.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Text, Markdown]

**Output Format:** [Markdown guidance with inline Aliyun CLI command examples and plain-text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate against Alibaba Cloud PDS and may require configured credentials, scoped permissions, and user confirmation for high-risk operations.]

## Skill Version(s):

0.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
