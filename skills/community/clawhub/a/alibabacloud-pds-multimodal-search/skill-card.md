## Description:

Implements exact filename search, fuzzy filename search, semantic file search, and image-based image search for Alibaba Cloud PDS drives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud storage operators use this skill to search, upload, download, and analyze files across Alibaba Cloud PDS enterprise, team, and personal spaces. It supports filename search, semantic file search, and image-based similar-image retrieval through Aliyun CLI and helper scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or update local Aliyun CLI tooling and plugins.

Mitigation: Review before installing, use verified Aliyun CLI and PDS plugin sources, and avoid curl-pipe-to-bash or global plugin updates in managed environments.

Risk: The skill can use persistent Alibaba Cloud credentials to access PDS resources.

Mitigation: Use least-privilege temporary credentials and verify the active CLI profile without exposing access keys or secrets.

Risk: The skill can upload local files, download PDS files, save signed analysis results, and generate local output files.

Mitigation: Require explicit approval before file transfer, analysis-result saving, or local output generation, and keep operations scoped to the user-selected PDS space.

## Reference(s):

- [PDS Drive Concepts and API Reference](references/drive.md)
- [PDS File Search](references/search-file.md)
- [Alibaba Cloud PDS Visual Similar Search Guide](references/visual-similar-search.md)
- [PDS Document and Audio/Video Analysis](references/multianalysis-file.md)
- [PDS File Upload Guide](references/upload-file.md)
- [PDS File Download Guide](references/download-file.md)
- [PDS Aliyun CLI Configuration Guide](references/config.md)
- [RAM Permission Requirements](references/ram-policies.md)
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and generated local file paths when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Aliyun CLI invocations, search result summaries, formatted analysis text, JSON query payloads, downloaded files, uploaded file confirmations, and optional PPTX or text outputs.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
