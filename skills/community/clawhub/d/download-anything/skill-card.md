## Description:

Find and download digital resources from URLs and resource directories, including ebooks, papers, media, software, cloud-drive links, torrents, and public media assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hacklyc](https://clawhub.ai/user/hacklyc)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to choose download tools, search resource directories, and generate shell-command workflows for retrieving authorized digital content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct users toward piracy-associated sources, rotating mirrors, torrents, and cloud-drive search engines.

Mitigation: Use the skill only for content the user is authorized to access, and avoid piracy-oriented source lists or mirror-hunting workflows.

Risk: The toolkit installer invokes package managers and may install multiple command-line tools through brew, pip, npm, apt, or dnf.

Mitigation: Review each command before execution and prefer pinned versions or operating-system-packaged dependencies over the bulk installer.

Risk: Some workflows use browser cookies or cookie-export options for authenticated downloads.

Mitigation: Avoid browser-cookie options unless using a dedicated low-risk browser profile and the download is authorized.

Risk: aria2 network-service patterns can expose remote-control download behavior if RPC is enabled insecurely.

Mitigation: Do not expose aria2 RPC; keep any download automation bound to trusted local interfaces with appropriate access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hacklyc/skills/download-anything)
- [Cloud Drive Search](references/cloud-search.md)
- [Ebooks, Academic Papers & Comics](references/ebooks.md)
- [Educational Resources](references/education.md)
- [Media Assets: Images, Video, Audio & Fonts](references/media-assets.md)
- [Music & Audio Downloads](references/music.md)
- [Search Techniques & Direct Link Extraction](references/search-techniques.md)
- [Software Downloads](references/software.md)
- [CLI Tools Reference](references/tools-reference.md)
- [Video, Film & TV Downloads](references/video.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and reference links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local command execution and file downloads; users should review commands before running them.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
