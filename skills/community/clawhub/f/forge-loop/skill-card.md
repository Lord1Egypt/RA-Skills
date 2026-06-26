## Description: <br>
Forge orchestrates a repair-inspect loop for multiple code fixes with independent inspection, dependency-aware parallel execution, protected-file guardrails, and crash-recoverable state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[melody1015](https://clawhub.ai/user/melody1015) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate batches of bug fixes, audit findings, or review recommendations through repair agents and independent inspection before acceptance. It is most useful when tasks have dependencies, need repeatable verification, or require guardrails around protected files and deletion checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can coordinate automated code changes across a repository. <br>
Mitigation: Run it on a clean branch or disposable checkout, review generated task files and diffs, and keep protected-files.txt current for sensitive files. <br>
Risk: Automatic commits may accept changes before a human has reviewed the final diff. <br>
Mitigation: Disable or avoid automatic commits unless that behavior is explicitly desired, and run the pre-commit safety check before accepting results. <br>
Risk: Summary and doc-sync behavior can execute project-local scripts. <br>
Mitigation: Use those features only in trusted repositories or after reviewing the local scripts they may run. <br>


## Reference(s): <br>
- [Forge protocol](artifact/references/protocol.md) <br>
- [ClawHub release page](https://clawhub.ai/melody1015/forge-loop) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON task/result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates project-side state, task, result, summary, reflection, and optional protected-file configuration files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
