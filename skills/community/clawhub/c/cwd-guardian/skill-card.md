## Description:

Monitors and restores the evolver process working directory. Use when evolver crashes with uv_cwd ENOENT errors or when the evolver process loses its cwd.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foras910521-lab](https://clawhub.ai/user/foras910521-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check an OpenClaw evolver workspace before daemon startup and stamp process/path state for watchdog workflows. It is most relevant when investigating uv_cwd ENOENT crashes or missing working-directory state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation overstates recovery behavior for restoring a missing working directory or restarting evolver.

Mitigation: Treat the skill as a workspace/state verification helper until the implementation is fixed and confirm recovery behavior in a controlled environment before relying on it.

Risk: The implementation writes persistent process/path state under a hardcoded OpenClaw workspace path.

Mitigation: Review whether that path is appropriate for the target environment and adjust or sandbox execution before installation.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a JSON state file under a hardcoded OpenClaw workspace path when executed.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
