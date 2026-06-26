## Description: <br>
Query and manage farm work orders and tasks. View assignments, create tasks, update status. Uses integration endpoints (no auth) for reads and authenticated endpoints for writes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianppetty](https://clawhub.ai/user/brianppetty) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Farm managers and operations teams use this skill to query task summaries and assignments, create work orders, update task status, and capture restock or follow-up work from natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated actions can create, assign, or update FarmOS task records. <br>
Mitigation: Require explicit user confirmation before every write action and use the least-privileged role allowed by the local role mapping. <br>
Risk: The skill depends on a trusted FarmOS endpoint, local auth helper, and local role file. <br>
Mitigation: Install only in environments where those local components are trusted and periodically review the role mapping for excess privileges. <br>
Risk: Broad task detection and cross-module lookups can add unrelated operational context. <br>
Mitigation: Limit cross-module lookups to cases the user requested or where the extra context is clearly needed for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brianppetty/farmos-tasks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with task summaries, confirmation prompts, curl examples, and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include FarmOS API calls for reads and authenticated task writes after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
