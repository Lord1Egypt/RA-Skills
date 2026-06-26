## Description: <br>
Track tasks in ClickUp from an AI agent - check open tasks before starting work, log completed work after, and capture future ideas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dyagil](https://clawhub.ai/user/dyagil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to maintain ClickUp task records for non-trivial work, completed actions, and future ideas. It helps an agent check existing tasks before work begins and record outcomes after meaningful work is finished. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task names and descriptions can store work details in ClickUp, including information the user did not intend to place in an external service. <br>
Mitigation: Avoid putting secrets, credentials, personal data, regulated data, or confidential project details in ClickUp tasks unless the user explicitly intends that storage. <br>
Risk: The workflow depends on a local ClickUp CLI/helper and user-provided workspace configuration. <br>
Mitigation: Inspect the local cu/cu.cjs helper and verify the ClickUp token and workspace list IDs before relying on the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dyagil/dyagil-clickup) <br>
- [ClickUp API](https://clickup.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directs agents to use a local ClickUp CLI for todo, done, and ideas task workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
