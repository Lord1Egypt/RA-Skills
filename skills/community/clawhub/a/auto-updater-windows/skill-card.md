## Description: <br>
Set up and maintain automatic OpenClaw + skill updates on Windows/macOS/Linux. Use when a user asks for scheduled updates, manual update runs, update health checks, or update summaries. On Windows, enforce native Windows/Git Bash flow and avoid WSL bash paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leo220yuyaodog](https://clawhub.ai/user/leo220yuyaodog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure manual or scheduled OpenClaw and skill updates across Windows, macOS, and Linux. It is especially focused on Windows-native update execution with Git Bash/MSYS rather than WSL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk or scheduled updates can change OpenClaw and installed skills without the user reviewing each package at execution time. <br>
Mitigation: Confirm the update schedule before enabling automation, keep a rollback plan for local edits, and report updated, unchanged, and failed items after each run. <br>
Risk: Using the wrong Windows shell path can route update steps through WSL instead of the intended native Windows/Git Bash flow. <br>
Mitigation: Verify `where.exe bash` and `bash --version` before build steps, and ensure Git Bash/MSYS is first in PATH when bash is needed. <br>
Risk: Force-updating a skill can overwrite local modifications. <br>
Mitigation: Use forced skill updates only after explicit user approval and keep the normal all-skill update flow non-force by default. <br>


## Reference(s): <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Concise update summaries listing updated, unchanged, and failed items.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
