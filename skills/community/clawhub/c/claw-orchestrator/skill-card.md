## Description: <br>
CC Agent 分析 + WBClaw 执行协作编排器。将任务发送给 Claude Code Agent 做前置分析设计，再由 WorkBuddy Claw 执行落地，自动生成执行报告。适用于需要深度分析+工程执行的多步骤任务。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zenyang-x](https://clawhub.ai/user/zenyang-x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate a Claude Code analysis and file-generation step with a WorkBuddy Claw execution, preview, reporting, and memory-update step for multi-stage implementation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run a write-capable agent with bypassed permissions in a configured local workspace. <br>
Mitigation: Review and change the configured paths before use, run it only in a disposable or version-controlled directory, and inspect generated or modified files before relying on them. <br>
Risk: Task text may influence generated commands or file writes. <br>
Mitigation: Avoid untrusted task text and treat bypassPermissions as elevated access that can change local files without normal prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zenyang-x/claw-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports, command-line status text, and generated task files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write task_report.md, MEMORY.md entries, daily log entries, and task-specific HTML, Python, or Markdown files in the configured workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
