## Description:

Guides agents in formatting Feishu @mentions for text, rich text, and interactive card messages so mentions trigger correctly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vision-qiu](https://clawhub.ai/user/vision-qiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators who prepare Feishu bot or app messages use this skill to choose the correct @mention syntax for text, rich text, and interactive card messages, including mentions of specific members or everyone in a chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Looking up Feishu chat members when an open_id is missing can expose chat member identity data to the active Feishu integration.

Mitigation: Use the skill only in workspaces where the agent is allowed to prepare Feishu messages and access member identity data for the target chat.

Risk: Using @everyone or the wrong mention format may fail or notify a broader group than intended.

Mitigation: Confirm the target message type, recipient identifiers, and chat permissions before sending Feishu messages that include mentions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, JSON, Shell commands]

**Output Format:** [Markdown guidance with JSON snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes separate Feishu mention formats for text, rich text, and interactive card messages.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
