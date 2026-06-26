## Description: <br>
Checks messages received by an Aicoo agent, including direct messages, shared-agent conversations, pending network requests, contacts, timestamps, unread state, and suggested follow-up actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xisen-w](https://clawhub.ai/user/xisen-w) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Aicoo users use this skill to review messages and conversation history received by their agent, including direct messages, shared-agent inbox activity, and pending network requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can display private Aicoo messages and contact details from broad prompts without a built-in confirmation step. <br>
Mitigation: Use explicit Aicoo inbox wording, avoid shared or visible sessions, and review output before exposing or acting on message content. <br>
Risk: The skill requires AICOO_API_KEY and may use it to access Aicoo inbox data. <br>
Mitigation: Install only when inbox access is intended and prefer a narrowly scoped API key if Aicoo supports one. <br>


## Reference(s): <br>
- [Check Messages on ClawHub](https://clawhub.ai/xisen-w/check-messages) <br>
- [Publisher profile](https://clawhub.ai/user/xisen-w) <br>
- [Aicoo API base URL](https://www.aicoo.io/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized inbox results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include private Aicoo message content, contact details, timestamps, unread status, and suggested follow-up actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
