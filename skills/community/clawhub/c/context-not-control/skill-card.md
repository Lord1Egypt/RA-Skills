## Description: <br>
Enable "Context, not Control" workflow - clarify requirements through multi-turn dialogue, reduce rework, and execute with appropriate permission levels. Use when users want AI to take more autonomy, need help clarifying vague requirements, or want to establish trust-based collaboration patterns. Supports three permission levels (Master/Collaborative/Assistant) and automatic context management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[843645440](https://clawhub.ai/user/843645440) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to clarify vague project requirements, choose an autonomy level, and maintain reusable project context and permission boundaries for future agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill promotes a higher-autonomy workflow that can allow broad file changes, persistent jobs, external notifications, or database updates without enough approval. <br>
Mitigation: Use the Collaborative or Assistant permission level by default, keep helper scripts scoped to the intended workspace context files, and require explicit approval for persistent jobs, webhooks, database or schema changes, production-impacting actions, and writes outside the project context. <br>


## Reference(s): <br>
- [Clarification Framework](references/clarification-framework.md) <br>
- [Permission Levels](references/permission-levels.md) <br>
- [Examples](references/examples.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with optional JSON output and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts can create or update PROJECT.md and PERMISSION_CONFIG.yaml in the selected workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact Version section) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
