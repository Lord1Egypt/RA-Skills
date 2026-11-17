## Description:

Downloads Chinese ebooks to a user's computer by searching third-party resource sites, resolving CTFile links, downloading ZIP archives, and extracting common ebook formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoyishuai](https://clawhub.ai/user/caoyishuai)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask an agent to search third-party ebook sources, retrieve cloud-drive links, download archives, and extract EPUB, AZW3, MOBI, PDF, or TXT files to a local computer when they are authorized to download the content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates downloads from third-party ebook and file-sharing sources, which can retrieve content the user is not authorized to download.

Mitigation: Require explicit user confirmation before download or extraction and use the workflow only for content the user is authorized to access.

Risk: The provided shell and Python templates may be unsafe if raw book titles or remote URLs are inserted directly.

Mitigation: Rewrite commands with validated URLs, safe filenames, fixed output directories, and quoted arguments before execution.

Risk: Downloaded archives may contain unexpected files or excessive extracted content.

Mitigation: Validate the archive type and enforce extraction limits before writing files to the user's computer.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/caoyishuai/skills/ebook-downloader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline shell and Python code blocks, plus downloaded ebook files when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce EPUB, AZW3, MOBI, PDF, or TXT files extracted from downloaded ZIP archives.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
