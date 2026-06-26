## Description: <br>
Use when another skill returns Feishu display payloads or messageToolCalls; this skill teaches the agent to use the OpenClaw message tool to send Feishu cards, text, and media in the current conversation, then reply with NO_REPLY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yqxu](https://clawhub.ai/user/yqxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill when another skill produces Feishu display payloads that should be sent as cards, text, or media in the active conversation without rewriting or summarizing the content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted upstream messageToolCalls could send unintended Feishu card, text, or media content. <br>
Mitigation: Install this skill only with trusted payload-producing skills or tools, and review the upstream workflow before deployment. <br>
Risk: Media payloads that include file paths may share unintended files if the upstream payload source is not trusted. <br>
Mitigation: Limit use to trusted upstream payload sources and review file-sending behavior in the calling skill or tool. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yqxu/feishu-card-display) <br>
- [Project homepage](https://github.com/AIDiyTeams/claw-skill/tree/main/feishu-card-display) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Feishu message tool calls followed by the string NO_REPLY] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves upstream card, text, and media payloads exactly as provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
