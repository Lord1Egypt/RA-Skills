## Description:

Summarizes Feishu/Lark docx or wiki documents that the user can read, using a fixed summary schema from agent memory and returning the result in the current chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[victor-thu](https://clawhub.ai/user/victor-thu)

### License/Terms of Use:


## Use Case:

External users and knowledge workers use this skill to summarize Feishu/Lark documents from docx or wiki links without writing a custom prompt. It is intended for documents the user has permission to read and for summaries that follow the user's stored template.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads full Feishu/Lark documents and summarizes their contents into the current chat.

Mitigation: Use it only for documents the user is comfortable having read in full and summarized in the active conversation.

Risk: The skill consults persistent memory for the summary template, which may introduce unrelated private details if that memory is not tightly scoped.

Mitigation: Keep the memory-stored summary template limited to formatting preferences and free of unrelated sensitive information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/victor-thu/skills/feishu-doc-summarizer)
- [Publisher profile](https://clawhub.ai/user/victor-thu)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summary in the current chat]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the user's stored summary schema; missing fields are kept as unknown rather than removed.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
