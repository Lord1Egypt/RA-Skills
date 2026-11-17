## Description:

Generates Feishu weekly reports by collecting work material from Feishu chat messages and local daily memory logs, then organizing it into a weekly report template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hakityc](https://clawhub.ai/user/hakityc)

### License/Terms of Use:


## Use Case:

Employees and teams use this skill to turn Feishu chat history and local daily work notes into concise weekly summaries, outcomes, next-week plans, and support requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses Feishu app credentials and private chat history.

Mitigation: Install only when this access is intended, restrict the Feishu app to minimum message-read scopes, and avoid printing or passing app_secret on the command line.

Risk: Weekly reports or retained memory files may expose sensitive work details.

Mitigation: Confirm chat IDs and date ranges before each run, and review or delete memory files that may retain sensitive work details.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown weekly report with supporting shell commands and JSON Lines message collection output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include summarized sensitive work details from Feishu chats or local memory logs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
