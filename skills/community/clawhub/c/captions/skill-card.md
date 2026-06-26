## Description: <br>
Fetches timestamped captions, subtitles, and spoken text from YouTube videos using TranscriptAPI for reading, quoting, translation, accessibility, content review, and language learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[therohitdas](https://clawhub.ai/user/therohitdas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, accessibility reviewers, educators, and content analysts use this skill to retrieve YouTube captions or transcripts for reading, quoting, translation, accessibility checks, content review, and language learning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends YouTube video references to TranscriptAPI. <br>
Mitigation: Use it only for videos you are comfortable sharing with TranscriptAPI, and avoid submitting private or sensitive video URLs. <br>
Risk: Setup can involve account signup, OTPs, API keys, temporary secret files, and persistent credential storage. <br>
Mitigation: Prefer creating the account yourself, store the API key in a trusted secret manager, avoid pasting keys or OTPs into ordinary chat when a secure secret-entry path exists, and revoke the key when you stop using the skill. <br>


## Reference(s): <br>
- [TranscriptAPI](https://transcriptapi.com) <br>
- [TranscriptAPI Auth Setup](references/auth-setup.md) <br>
- [Captions on ClawHub](https://clawhub.ai/therohitdas/captions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with curl commands and JSON or plain-text transcript responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRANSCRIPT_API_KEY and sends YouTube video references to TranscriptAPI.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
