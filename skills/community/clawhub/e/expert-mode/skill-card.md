## Description: <br>
Expert Mode helps an agent update and search a catalog of expert personas, activate a selected expert response style, and manage custom or favorite experts with confirmation-gated persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[syx1989](https://clawhub.ai/user/syx1989) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to maintain an expert-mode catalog, find relevant expert personas, and switch the agent into a selected expert style for task-specific guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Activating expert personas can change the agent's future response style. <br>
Mitigation: Load expert configurations only from the local trusted list and activate a persona only when the user requests it. <br>
Risk: Catalog updates can write expert entries into MEMORY.md. <br>
Mitigation: Show an update preview and require explicit user confirmation before any persistent write. <br>
Risk: Network updates can fetch external expert lists or mirror content. <br>
Mitigation: Keep automatic sync disabled unless needed, prefer official GitHub sources over mirrors, and validate fetched content before accepting updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/syx1989/expert-mode) <br>
- [Expert Mode reference](references/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown responses with confirmation prompts, update previews, and expert-mode guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose MEMORY.md updates only after user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
