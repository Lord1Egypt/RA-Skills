## Description: <br>
Organizes Feishu wiki content by analyzing document titles and selected content, then proposing and executing user-approved moves into clearer knowledge-base categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgugeng](https://clawhub.ai/user/lgugeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, knowledge managers, and operations teams use this skill to classify Feishu wiki documents, create folder structures, and move documents after reviewing a preview plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant an agent broad authority to move Feishu wiki documents. <br>
Mitigation: Start with one knowledge base and review every preview plan before approving document moves. <br>
Risk: Cross-library, merge, or failed-move handling could place documents in unexpected locations. <br>
Mitigation: Avoid cross-library or merge operations unless explicitly requested, and confirm how failed items will be handled before execution. <br>
Risk: Hourly automation can continue making or proposing changes after the initial organizing task. <br>
Mitigation: Do not enable hourly automation until the disable process, log locations, and protected status files are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lgugeng/feishu-wiki-organizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Feishu API call examples and structured move plans.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user approval before document moves and may produce local move logs or status files when automation is enabled.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
