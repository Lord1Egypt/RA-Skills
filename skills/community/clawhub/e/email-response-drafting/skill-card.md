## Description: <br>
Drafts email replies with tone matching, proper threading, email-client-safe formatting, and a draft-first approval pattern. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill to draft individual email replies that match the thread's tone, preserve reply threading, and remain reviewable before sending. It is scoped to response drafting, not marketing campaigns or mass outreach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email drafts could be sent or saved before the user has confirmed recipients, subject, and body. <br>
Mitigation: Follow the skill's draft-first workflow: present the draft for review, ask for explicit confirmation when intent is ambiguous, and send only after direct approval. <br>
Risk: A reply can break email threading if the original message is not found. <br>
Mitigation: Verify the original message and message ID before creating a threaded reply; if unavailable, tell the user instead of silently creating a standalone draft. <br>
Risk: Markdown email content can render incorrectly across email clients. <br>
Mitigation: Convert Markdown to email-safe HTML where needed, include a plain-text body, and avoid formatting patterns called out by the skill as fragile. <br>


## Reference(s): <br>
- [Email Agent MCP](https://github.com/UseJunior/email-agent-mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/stevenobiajulu/email-response-drafting) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown email drafts and concise drafting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include YAML frontmatter for saved draft files and threading metadata when the user requests a file-backed draft.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
