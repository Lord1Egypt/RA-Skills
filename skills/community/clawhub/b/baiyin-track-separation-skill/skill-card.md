## Description: <br>
音轨分离能力，支持人声伴奏分离。Use when: (1) 用户需要将音频分离为人声和伴奏，(2) 用户需要对音频进行专业级别的音轨分离处理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiuping520](https://clawhub.ai/user/jiuping520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit audio for vocal and accompaniment separation through Baiyin/Hikoon APIs, then receive task status and result links for generated tracks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Baiyin API key and submits audio to Baiyin/Hikoon-hosted services. <br>
Mitigation: Install only when the user trusts Baiyin/Hikoon with both submitted audio and the API key; avoid using it for private recordings until upload, access, and retention practices are confirmed. <br>
Risk: The security summary says the skill tells the agent to silently self-update and to downplay external audio uploads. <br>
Mitigation: Require platform-controlled update handling or explicit user approval before updates, and make upload behavior clear during review and deployment. <br>
Risk: Generated result links may expose processed audio tracks to anyone who can access the URLs. <br>
Mitigation: Confirm link access controls and retention windows before processing confidential recordings, and download or delete results according to the service policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiuping520/baiyin-track-separation-skill) <br>
- [Baiyin Open Platform](https://ai.hikoon.com/) <br>
- [Track separation API endpoint](https://ai.hikoon.com/api/open/v1/track-separation/split) <br>
- [File upload API endpoint](https://ai.hikoon.com/api/open/v1/file/upload) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, API calls, guidance] <br>
**Output Format:** [Markdown with JSON, HTTP, shell, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task identifiers, processing status, vocal/accompaniment result URLs, and concise next-step guidance; must not reveal full API keys.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
