## Description: <br>
Downloads available Bilibili subtitles for a provided video URL, parses them into plain text, and helps an agent produce a structured video summary in Chinese or English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yeezi02](https://clawhub.ai/user/yeezi02) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to summarize Bilibili videos when subtitles are available. It is intended for subtitle retrieval, subtitle-to-text parsing, and concise structured summaries of video content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to expose and persist a live Bilibili session cookie, which can create account-security risk in an untrusted local agent environment. <br>
Mitigation: Use only in a trusted environment, manually create the cookie file with restrictive permissions when possible, use a low-risk account, and revoke or rotate the session after use. <br>


## Reference(s): <br>
- [Bilibili Cookie Setup Guide](references/cookie-setup.md) <br>
- [Bilibili](https://www.bilibili.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summary with optional shell command output and plain-text subtitle content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a locally stored Bilibili SESSDATA cookie for authenticated subtitle access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
