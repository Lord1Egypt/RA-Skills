## Description: <br>
Run Twitter/X research, monitoring, watchlists, and OAuth-gated posting through AIsa. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to research Twitter/X activity, monitor trends or watchlists, and publish approved posts through AIsa OAuth workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal authorize command output can expose the raw AISA_API_KEY. <br>
Mitigation: Do not paste authorize or post command output into chats, tickets, logs, or transcripts; rotate AISA_API_KEY if it has already been exposed. <br>
Risk: Twitter/X research, OAuth posting flow, post content, uploaded media, and the API key are handled by AIsa's relay. <br>
Mitigation: Install and run the skill only when the user trusts AIsa with that data, and send only media files the user explicitly selected for upload. <br>
Risk: The skill can publish externally to Twitter/X. <br>
Mitigation: Require explicit user approval before posting and do not claim success until the API returns a confirmed publish result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baofeng-tech/aisa-twitter-api-command-center-slot1) <br>
- [AIsa homepage](https://aisa.one) <br>
- [AIsa Twitter OAuth](references/post_twitter.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output from bundled Python clients] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; posting, OAuth authorization, and media upload requests are sent through AIsa.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
