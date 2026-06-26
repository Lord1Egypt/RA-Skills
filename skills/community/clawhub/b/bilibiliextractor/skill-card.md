## Description: <br>
Extracts subtitles from Bilibili videos and produces a structured summary of the main ideas, topics, and conclusions, with full transcript output when requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kongym1234](https://clawhub.ai/user/kongym1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill when a user provides a Bilibili URL or BV identifier and wants video captions extracted, summarized, or returned as a transcript. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send selected Bilibili video audio to SiliconFlow for transcription when captions are unavailable. <br>
Mitigation: Avoid using it for private or sensitive videos, and use normal Bilibili links or BV IDs for public videos. <br>
Risk: The included Python script requires access to a SiliconFlow API key from the agent environment. <br>
Mitigation: Store the key in the configured environment file and do not pass or invent plaintext API keys in commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kongym1234/bilibiliextractor) <br>
- [Publisher profile](https://clawhub.ai/user/kongym1234) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries or plain transcript text, with shell commands and configuration guidance when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to summarizing extracted captions; returns full transcript text only when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
