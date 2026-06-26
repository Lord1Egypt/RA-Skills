## Description: <br>
Use when operating inside one ALab experiment worktree with that worktree token context to inspect status, edit candidate source, run evaluations, submit final results, and read visible experiment evidence without project admin or root privileges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bebetterest](https://clawhub.ai/user/bebetterest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents operating an ALab experiment worktree use this skill to improve candidate source, run supported evaluations or direct submits, and report visible evidence while staying within worktree-token scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential or scope exposure if a worker accepts project admin or root keys, uses another worktree token, or prints raw token material. <br>
Mitigation: Use only the current worktree token context, keep project admin keys private and out of the worker session, and do not read, print, copy, commit, or rewrite raw tokens or keys. <br>
Risk: Privileged or destructive ALab operations could change project state outside the intended experiment scope. <br>
Mitigation: Treat project-level and root command surfaces as unavailable in the worker role, review destructive lifecycle actions before confirmation, and report required admin operations to a separate project-level or root-admin session. <br>
Risk: Hidden evaluator assets, hidden logs, secret files, or broad artifact contents may be sensitive or inaccessible to the worker. <br>
Mitigation: Use only visible evidence, avoid hidden logs and secret files, inspect artifacts only as needed, and keep explanatory details in visible logs or artifacts separate from machine-parsed reward files. <br>


## Reference(s): <br>
- [ALab Experiment Worker Commands](references/commands.md) <br>
- [ALab Experiment Worker Commands (Chinese)](references/commands_cn.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/bebetterest/alab-experiment-worker) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and concise final reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ALab command invocations, source edits, run evidence summaries, submit refs, and remaining-risk notes.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
