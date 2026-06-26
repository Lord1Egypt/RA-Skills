## Description: <br>
Connect FeedTo.ai to OpenClaw so browser feeds arrive through the FeedTo skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[isopenclaw](https://clawhub.ai/user/isopenclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to receive FeedTo browser feeds in OpenClaw through a persistent outbound listener with a polling fallback. It is intended for installations where feed content should be delivered into chat while preserving the reminder that feed payloads are untrusted external text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub FeedTo release page](https://clawhub.ai/isopenclaw/feedto) <br>
- [FeedTo service](https://feedto.ai) <br>
- [FeedTo API key settings](https://feedto.ai/settings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with inline shell commands and relayed feed content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FEEDTO_API_KEY, curl, and node; feed payloads are relayed verbatim and should be treated as untrusted external text.] <br>

## Skill Version(s): <br>
0.5.1 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
