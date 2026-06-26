## Description: <br>
Auto Skill Evolver improves local agent skills through trace and feedback-driven proposal, status, approval, and rollback workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyingzhuangk](https://clawhub.ai/user/zhangyingzhuangk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to run local training and evolution loops for agent skills, review proposed diffs, check proposal status, approve changes, and roll back prior skill versions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run user-chosen local commands and modify local skill files. <br>
Mitigation: Use it in a development or isolated skills directory, set allowed skill roots when possible, review the printed diff, and approve only intentional changes. <br>
Risk: Execution traces and feedback may contain secrets or untrusted content. <br>
Mitigation: Keep traces free of secrets and rely on the proposal-first workflow, secure workspace handling, and prompt-isolation guidance before applying updates. <br>
Risk: Plain yes approval is easier to misuse than proposal-specific approval. <br>
Mitigation: Prefer hash-based approval or token-file approval, and use proposal expiry for deferred approval flows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangyingzhuangk/auto-skill-evolver-1-5-1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, unified diffs, JSON status events, proposed skill files, and shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write proposal files, proposal metadata, checkpoints, last_update.md, and history.md during approved local workflows.] <br>

## Skill Version(s): <br>
1.5.1 (source: artifact/SKILL.md frontmatter; ClawHub release package version 1.0.0 from evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
