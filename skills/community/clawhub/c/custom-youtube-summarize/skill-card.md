## Description: <br>
Extract transcript from a YouTube video using Python and summarize it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[5eun](https://clawhub.ai/user/5eun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill when a user provides a YouTube URL and asks for a summary or explanation. The skill retrieves available subtitles, returns the transcript text, and guides the agent to summarize the transcript. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network requests to YouTube to retrieve transcript content. <br>
Mitigation: Use it only in environments where outbound requests to YouTube are allowed and expected. <br>
Risk: Retrieved transcript text is passed to the LLM for summarization. <br>
Mitigation: Avoid using the skill for sensitive private video content unless that data flow is approved. <br>
Risk: Bundled transcript libraries include proxy support outside the documented skill flow. <br>
Mitigation: Do not provide proxy credentials unless proxy use is intentional and separately approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/5eun/custom-youtube-summarize) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with transcript markers and natural-language summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Python script to fetch YouTube transcripts, preferring Korean and falling back to English when available.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
