## Description: <br>
Orchestrates software development by coordinating with Cursor Agent, managing git workflows, and ensuring quality delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[47vigen](https://clawhub.ai/user/47vigen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate feature work, bug fixes, refactors, git workflow steps, build verification, deployment pipeline monitoring, and final delivery reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can coordinate real git changes, including staging, committing, pushing, merging, and deployment-related steps. <br>
Mitigation: Use only in repositories where the user is authorized to make changes; require the agent to stop before git write operations or deployment actions; prefer pull requests, branch protections, and human review of the final diff. <br>
Risk: The workflow forwards user-provided links and attachments to Cursor. <br>
Mitigation: Filter links and attachments before forwarding, and do not provide secrets, customer data, private configuration, credentials, or sensitive internal material. <br>
Risk: Build and deployment monitoring may affect release workflows if the agent is allowed to continue without review. <br>
Mitigation: Keep deployment credentials and pipeline triggers permissioned, run work on controlled branches, verify builds before merge, and require explicit approval for release-impacting steps. <br>


## Reference(s): <br>
- [Workflow Details](references/workflow-details.md) <br>
- [Model Selection Matrix](references/model-selection.md) <br>
- [Cursor Interaction Guidelines](references/cursor-guidelines.md) <br>
- [Final Report Template](references/report-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/47vigen/developer-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, code/configuration snippets, implementation plans, and final reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May coordinate Cursor prompts, git commands, build and deployment checks, and structured delivery reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
