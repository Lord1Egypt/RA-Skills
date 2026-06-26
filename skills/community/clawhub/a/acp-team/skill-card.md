## Description: <br>
Team coordination layer for multi-agent workflows with mailbox, task board, and lease-based task management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[femto](https://clawhub.ai/user/femto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multiple AI agents through shared task boards, message inboxes, role-based spawning, and lease-based task claiming. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses global npm tools and local .team/ and .tasks/ files in a project. <br>
Mitigation: Install only in trusted environments and review local team and task files before using them in sensitive projects. <br>
Risk: Spawned agents may receive broad prompts or access task and message content. <br>
Mitigation: Use explicit prompts, keep secrets out of tasks and messages, monitor spawned agents, and shut down team members when finished. <br>


## Reference(s): <br>
- [acp-team on ClawHub](https://clawhub.ai/femto/acp-team) <br>
- [acp-team npm package](https://www.npmjs.com/package/acp-team) <br>
- [acpx GitHub repository](https://github.com/openclaw/acpx) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with command examples, tables, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for local team coordination using acp-team, acpx, .team/ inbox files, and .tasks/ task files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
