## Description: <br>
Guides agents through coordinator, fork, and swarm coordination patterns for multi-agent coding workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to choose an appropriate multi-agent delegation pattern, coordinate task ownership, isolate worker workspaces, and synthesize worker outputs before implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying the examples can expose project context to external agent or model CLIs. <br>
Mitigation: Redact secrets and proprietary material before passing synthesis documents, task files, or diffs to external tools. <br>
Risk: Worker agents may create or modify coordination files, claim locks, worktrees, mailbox files, and review artifacts. <br>
Mitigation: Use a trusted version-controlled workspace, limit worker tool permissions, and inspect `.coordination`, `.claims`, `.worktrees`, and mailbox files before relying on results. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lanyasheng/eh-multi-agent) <br>
- [Delegation Modes](references/delegation-modes.md) <br>
- [Task Coordination](references/task-coordination.md) <br>
- [File Claim Lock](references/file-claim-lock.md) <br>
- [Workspace Isolation](references/workspace-isolation.md) <br>
- [Synthesis Gate](references/synthesis-gate.md) <br>
- [Review-Execution Separation](references/review-execution-separation.md) <br>
- [Extended Patterns](references/extended-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON snippets, shell command examples, and configuration patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; examples may create coordination files, file locks, worktrees, mailbox files, and review artifacts when applied by an agent.] <br>

## Skill Version(s): <br>
2.4.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
