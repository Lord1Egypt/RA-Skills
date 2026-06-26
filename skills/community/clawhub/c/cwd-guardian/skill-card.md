## Description: <br>
Monitors and restores the evolver process working directory when evolver crashes with uv_cwd ENOENT errors or loses its cwd. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foras910521-lab](https://clawhub.ai/user/foras910521-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check an OpenClaw evolver workspace, record guardian state, and recover from missing-working-directory failures that can stop the evolver process. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has a filesystem recovery side effect that can recreate a missing working-directory path and allow the associated daemon workflow to continue. <br>
Mitigation: Run it only in the intended workspace and review logs or confirmation controls around any recovery action before relying on the result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/foras910521-lab/cwd-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also emit console status messages and write local guardian state when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
