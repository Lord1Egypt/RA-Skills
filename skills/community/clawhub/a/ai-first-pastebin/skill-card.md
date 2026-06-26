## Description: <br>
Use 呵.tw as an AI-first pastebin to shorten URLs, store shareable agent handoff notes, recover tagged pastes, and reduce LLM token usage across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joustonhuang](https://clawhub.ai/user/joustonhuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create short links, store non-secret shareable handoff notes, retrieve tagged pastes, and reduce context-window usage across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text or URLs are sent to the hosted pastebin service. <br>
Mitigation: Use the skill only for shareable, non-secret content and review values passed through --stdin, --content, or URL-shortening commands before upload. <br>
Risk: URLs may contain tokens, private document links, internal hostnames, or sensitive query parameters. <br>
Mitigation: Strip sensitive URL parts or avoid shortening the URL when it points to private or confidential material. <br>


## Reference(s): <br>
- [呵.tw agent-facing documentation](https://呵.tw/llms.txt) <br>
- [ClawHub skill page](https://clawhub.ai/joustonhuang/ai-first-pastebin) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user-selected URL, paste, metadata, chain, search, and QR helper outputs from the hosted service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
