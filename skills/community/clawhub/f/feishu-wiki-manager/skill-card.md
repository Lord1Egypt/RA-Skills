## Description: <br>
Feishu Wiki Manager helps an agent browse, search, create, move, rename, and organize Feishu/Lark Wiki spaces and nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[young-joey](https://clawhub.ai/user/young-joey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge managers, and workspace operators use this skill to have an agent navigate Feishu/Lark Wiki spaces, search knowledge base content, and plan or execute confirmed node creation, movement, renaming, and structure cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Wiki searches or edits may expose or alter more workspace content than intended. <br>
Mitigation: Use an account with only the permissions needed, review search scope before broad searches, and confirm create, move, or rename plans before execution. <br>
Risk: Batch node changes can trigger rate limits or make large structural changes difficult to review. <br>
Mitigation: Keep batch operations small, execute them serially, and show a concise change summary after completion. <br>


## Reference(s): <br>
- [Wiki structure templates](artifact/references/wiki-templates.md) <br>
- [ClawHub skill page](https://clawhub.ai/young-joey/feishu-wiki-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, API Calls] <br>
**Output Format:** [Markdown text with structured action plans, summaries, and Feishu Wiki action calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Modification workflows should confirm create, move, and rename plans with the user before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
