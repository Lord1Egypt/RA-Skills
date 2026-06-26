## Description: <br>
Respond to user requests for AIOZ Stream API. Use provided scripts to upload videos, fetch analytics, manage media, and create livestreams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[namle-aioz](https://clawhub.ai/user/namle-aioz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to manage AIOZ Stream media workflows, including video uploads, livestream key creation, media lookup, balance checks, and analytics retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate an AIOZ Stream account using user-provided API keys. <br>
Mitigation: Use a dedicated or least-privileged API key when available and install the skill only when account operations are intended. <br>
Risk: Secret keys may be exposed if pasted into chat, commands, logs, or shell history. <br>
Mitigation: Provide credentials through environment variables or a secret manager and avoid placing raw secrets in sample commands or responses. <br>
Risk: A wrong local video path or title could upload unintended media. <br>
Mitigation: Confirm the exact file path and title before running upload commands. <br>
Risk: Uploaded media may remain in transcoding before playback URLs are available. <br>
Mitigation: Report the current status and ask the user to check again later when URLs are not yet present. <br>


## Reference(s): <br>
- [AIOZ Stream API Reference](references/api_reference.md) <br>
- [AIOZ Stream API Base URL](https://api.aiozstream.network/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/namle-aioz/aioz-stream-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STREAM_PUBLIC_KEY and STREAM_SECRET_KEY environment variables; scripts use curl, jq, md5sum, file, stat, and date.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
