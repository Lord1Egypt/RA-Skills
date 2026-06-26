## Description: <br>
Transcribes spoken audio from Douyin video share text or links into text, and can check dy-caption credits and transcription history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xwchris](https://clawhub.ai/user/xwchris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content teams use this skill to submit Douyin share text or links for transcription, then retrieve transcript text, account credit balance, or recent transcription history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Douyin share content and a dy-caption API key to an external transcription service. <br>
Mitigation: Install only if you trust dy-caption and api.dycaption.cn; use a dedicated or revocable API key where possible. <br>
Risk: Private or sensitive video content may be exposed to the transcription service. <br>
Mitigation: Avoid submitting private or sensitive videos unless that data sharing is acceptable for the user's environment. <br>


## Reference(s): <br>
- [ClawHub dy-caption release page](https://clawhub.ai/xwchris/dy-caption) <br>
- [dy-caption API service](https://api.dycaption.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and returned transcription text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses DY_CAPTION_API_KEY and sends Douyin share content to api.dycaption.cn.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
