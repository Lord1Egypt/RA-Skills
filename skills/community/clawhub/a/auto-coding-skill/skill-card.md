## Description: <br>
Auto Coding V3 is an autonomous coding workflow skill that uses staged sub-agent prompts, model selection, review vetoes, complexity grading, and risk scorecards to move software tasks from requirements through implementation and verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krislu1221](https://clawhub.ai/user/krislu1221) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to structure coding work into design, decomposition, coding, testing, review, optimization, verification, and final output stages. It is intended for repository-level software changes where staged progress reporting, approval rules, state recovery, and review checks are useful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad capability tags and approval controls that may allow consequential repository changes. <br>
Mitigation: Install only in trusted repositories, review the capability tags and .auto-coding/rules.yaml, and run the skill in a disposable branch or worktree for higher-risk architecture or deletion work. <br>
Risk: Local .auto-coding state, logs, approvals, and scratchpad files may contain task details, file paths, test output, or code excerpts. <br>
Mitigation: Keep .auto-coding out of commits, avoid use with secrets or confidential code unless the model provider is approved, and delete the directory when the task is complete. <br>


## Reference(s): <br>
- [Auto Coding V3 ClawHub page](https://clawhub.ai/krislu1221/auto-coding-skill) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [DESIGN.md](artifact/DESIGN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown progress reports, code edits, configuration files, shell commands, and verification summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local .auto-coding state, logs, approval records, and scratchpad files inside the project directory.] <br>

## Skill Version(s): <br>
3.7.17 (source: server release metadata, clawhub.json, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
