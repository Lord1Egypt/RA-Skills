## Description: <br>
Run Twitter/X research, monitoring, watchlists, and OAuth-gated posting through AIsa. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research Twitter/X accounts, monitor trends or watchlists, and prepare OAuth-gated posts through the AIsa relay after explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks this release suspicious because the OAuth posting client can expose the full AIsa API key in command output. <br>
Mitigation: Use only if AIsa is trusted with the API key, OAuth authorization, tweet text, and uploaded media; avoid CI, shared terminals, logged sessions, and notebooks until command output is redacted, and rotate any key that may have been exposed. <br>
Risk: The skill posts externally and can send local image or video files to the AIsa Twitter/X API endpoint. <br>
Mitigation: Publish only after explicit approval, upload only files the user intentionally provided, and do not claim success until the API confirms the post. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bibaofeng/aisa-twitter) <br>
- [AIsa homepage](https://aisa.one) <br>
- [AIsa API endpoint](https://api.aisa.one) <br>
- [AIsa Twitter OAuth reference](references/post_twitter.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and communicates with https://api.aisa.one for Twitter/X read, OAuth, posting, and approved media-upload workflows.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
