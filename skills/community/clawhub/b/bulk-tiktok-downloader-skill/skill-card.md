## Description:

Bulk download TikTok videos from a text file of URLs using yt-dlp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mes28io](https://clawhub.ai/user/mes28io)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install and run a local yt-dlp based workflow for downloading batches of authorized TikTok videos from a trusted URL list into a chosen folder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs yt-dlp locally.

Mitigation: Install it in an isolated virtual environment and consider pinning the dependency version before use.

Risk: The downloader processes whatever URLs are placed in the input file.

Mitigation: Use a URL list that you created or trust, and download only content you are authorized to save.

Risk: The output directory can fill with downloaded media files.

Mitigation: Set the output directory to a scoped folder with expected storage capacity.

## Reference(s):

- [Upstream README](artifact/references/upstream-readme.md)
- [ClawHub skill page](https://clawhub.ai/mes28io/skills/bulk-tiktok-downloader-skill)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and local command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file paths, successful and failed download counts, failed URLs, and likely failure reasons.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
