## Description:

Find and download files from Feishu chat history by filename.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephyb97](https://clawhub.ai/user/josephyb97)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to retrieve files from Feishu chat history when automatic downloads miss a file or an older shared file must be recovered by filename.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A remote Feishu filename containing path traversal characters can cause the downloaded file to be written outside the selected output folder.

Mitigation: Validate and normalize remote filenames, force the final save path to remain under the selected output directory, and avoid overwriting existing files by default.

Risk: The skill requires Feishu application credentials to list chat messages and download message resources.

Mitigation: Run with least-privilege Feishu credentials and use a non-sensitive output directory.

Risk: Dependencies are declared without a lockfile in the artifact evidence.

Mitigation: Pin dependencies with a lockfile before broad or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josephyb97/skills/feishu-doc-finder)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands and downloaded file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET credentials and writes matching Feishu files to a selected output directory.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
