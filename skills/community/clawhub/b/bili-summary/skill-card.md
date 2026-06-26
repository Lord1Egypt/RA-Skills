## Description: <br>
Download Bilibili videos, extract or transcribe subtitles, and generate AI-powered detailed summaries using Gemini 2.5 Flash. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lava-chen](https://clawhub.ai/user/lava-chen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to inspect Bilibili video metadata, extract subtitles or transcribe audio, download media, and generate detailed summaries for Bilibili videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video subtitles or transcripts may be sent to Gemini when AI summarization is used. <br>
Mitigation: Use summarization only for public or non-sensitive videos, and keep GEMINI_API_KEY scoped and stored locally. <br>
Risk: Downloaded audio, subtitle, transcript, summary, or video files may remain in the local output directory. <br>
Mitigation: Review and delete the bili-summary output directory after use when content should not be retained. <br>


## Reference(s): <br>
- [Bili Summary ClawHub Release](https://clawhub.ai/lava-chen/bili-summary) <br>
- [Google AI Studio API Keys](https://aistudio.google.com/app/apikey) <br>
- [Gemini 2.5 Flash API Endpoint](https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent) <br>
- [Bilibili Subtitle API Endpoint](https://api.bilibili.com/x/player/wbi/v2?aid={aid}&cid={cid}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Files] <br>
**Output Format:** [Command output plus JSON video metadata, plain text transcripts, Markdown-style summaries, and saved media or text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes outputs to a local bili-summary temp directory; Gemini summaries require GEMINI_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
