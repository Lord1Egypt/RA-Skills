## Description:

Search and download Bilibili videos using yt-dlp and httpx.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ecojust](https://clawhub.ai/user/ecojust)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to search Bilibili by keyword, collect video metadata, save structured search results, and download selected videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser cookie use can expose authenticated session material.

Mitigation: Avoid browser-cookie commands unless needed for quality access; prefer exported cookies scoped to Bilibili.

Risk: Download commands accept user-supplied URLs.

Mitigation: Only pass Bilibili video URLs or BV IDs and run the skill in a constrained workspace.

Risk: Mutable dependency installs and fallback public mirrors can change what code is installed.

Mitigation: Pin dependencies and use trusted package indexes when deploying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ecojust/skills/bilibili-video-search-and-download)
- [Bilibili video search API endpoint](https://api.bilibili.com/x/web-interface/search/type)
- [Bilibili website](https://www.bilibili.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and Python code; search results are saved as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create search.json and downloaded media files in a local downloads directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
