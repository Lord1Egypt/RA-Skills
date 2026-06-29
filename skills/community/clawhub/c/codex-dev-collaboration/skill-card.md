## Description: <br>
Openclaw Codex Collaboration provides guidance for coordinating Codex development runs, including invocation patterns, canary checks, task folders, prompt templates, validation, and handoff records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kmpanda011172](https://clawhub.ai/user/kmpanda011172) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project maintainers use this skill to guide agents running Codex against local repositories with pre-run canary checks, standardized prompts, run logs, validation checklists, and OpenClaw/Codex handoff records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Codex automation can modify local repositories and save prompts, diffs, logs, and test output in local run records. <br>
Mitigation: Use the skill only in repositories where workspace-write Codex automation is acceptable, run the documented canary check first, and review saved records before sharing or relying on them. <br>
Risk: Incorrect Codex command ordering or skipped validation can block execution or mark failed work as complete. <br>
Mitigation: Keep the documented argument order, require non-empty canary and result files, and treat nonzero exits or empty outputs as blocked. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and directory templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes commands for canary checks and local run records; review saved prompts, diffs, and logs before sharing or relying on them.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
