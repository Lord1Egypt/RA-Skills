## Description: <br>
Use when setting up, checking, writing, linting, or troubleshooting Brigade memory handoffs for a repo or agent workspace, especially when a user wants durable agent memory, handoff inboxes, cross-harness memory routing, or a safe first Brigade setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up, inspect, draft, lint, review, and troubleshoot Brigade memory handoffs in code repositories or agent workspaces. It is especially suited to teams that want local-first durable memory workflows across coding harnesses while preserving existing memory conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill suggests shell commands that can install Brigade tooling or write Brigade setup files in a workspace. <br>
Mitigation: Run the dry-run quickstart first, inspect the planned files, and execute the non-dry-run command only after the target path and harness selection are confirmed. <br>
Risk: Handoff content may contain private workspace details, transcripts, terminal logs, or other sensitive material. <br>
Mitigation: Redact private hostnames, tokens, repo names, absolute home paths, user IDs, channel IDs, and raw private messages before sharing or committing output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/solomonneas/brigade-handoffs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and text code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be reviewed before execution, with dry-run results checked before workspace changes are made.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
