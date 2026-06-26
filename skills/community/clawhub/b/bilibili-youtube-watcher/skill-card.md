## Description: <br>
Fetch and read transcripts from YouTube and Bilibili videos for summarization, question answering, and information extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donnycui](https://clawhub.ai/user/donnycui) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and other external users can use this skill to fetch available subtitles from user-provided YouTube or Bilibili videos, then summarize the transcript, answer questions about the content, or extract relevant information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts YouTube or Bilibili through yt-dlp for URLs the user asks it to analyze. <br>
Mitigation: Use it only for videos the user intentionally provides and expects the agent to access. <br>
Risk: Troubleshooting with browser cookies can expose a logged-in browser session to yt-dlp. <br>
Mitigation: Avoid browser-cookie commands unless the user explicitly chooses that access pattern and understands the account-session implications. <br>
Risk: Video availability, region restrictions, rate limits, or missing subtitles can prevent transcript retrieval. <br>
Mitigation: Surface retrieval failures clearly and ask the user for another URL, language code, proxy setup, or manually supplied transcript when subtitles are unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/donnycui/bilibili-youtube-watcher) <br>
- [donnycui publisher profile](https://clawhub.ai/user/donnycui) <br>
- [yt-dlp project](https://github.com/yt-dlp/yt-dlp) <br>
- [Source inspiration: youtube-watcher](https://clawhub.ai/Michaelgathara/youtube-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain transcript text with markdown-style metadata headers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires yt-dlp on PATH; accepts a YouTube or Bilibili URL and optional subtitle language code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
