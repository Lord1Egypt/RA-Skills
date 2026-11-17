## Description: <br>
Helps an agent manage Feishu (Lark) calendars by listing, searching, checking schedules, and syncing events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Office users, developers, and automation agents can use this skill to work with Feishu/Lark calendars, including listing events, searching schedules, checking conflicts, and syncing event data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests command execution and local file search capabilities that are broader than its calendar purpose explains. <br>
Mitigation: Review the skill before installation and grant access only in environments where shell execution and local file search are acceptable. <br>
Risk: Calendar credentials and event details may be read or synced through Feishu/Lark APIs. <br>
Mitigation: Use narrowly scoped calendar credentials and avoid granting broad calendar access unless the deployment context requires it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
