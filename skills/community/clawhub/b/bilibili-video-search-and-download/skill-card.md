## Description: <br>
Search and download Bilibili videos using yt-dlp and httpx. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ecojust](https://clawhub.ai/user/ecojust) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and external users use this skill to search Bilibili by keyword, collect video metadata, save structured search results, and download selected videos through Python tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The downloader can accept URLs beyond Bilibili through yt-dlp. <br>
Mitigation: Review URLs before execution and restrict use to intended Bilibili video pages or BV identifiers. <br>
Risk: Authenticated downloads may use browser cookies from Chrome. <br>
Mitigation: Avoid browser-cookie access unless explicitly needed; prefer a narrowly scoped exported cookies file for authenticated downloads. <br>
Risk: The skill can install Python dependencies, contact network services, and write media files locally. <br>
Mitigation: Run in a virtual environment, review dependency installation commands, and choose an expected working directory before download. <br>


## Reference(s): <br>
- [Bilibili search API endpoint](https://api.bilibili.com/x/web-interface/search/type) <br>
- [Bilibili video page format](https://www.bilibili.com/video/BV1qD4y1U7fs) <br>
- [ClawHub skill page](https://clawhub.ai/ecojust/bilibili-video-search-and-download) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Files] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets; generated files may include JSON search results and downloaded media.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled scripts can write search.json and media files under downloads/ and can contact Bilibili or other URLs accepted by yt-dlp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
