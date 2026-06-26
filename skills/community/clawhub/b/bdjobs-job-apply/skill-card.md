## Description: <br>
BDJobs job search, matching, applying, undoing, and salary-update automation for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sazidulalam47](https://clawhub.ai/user/sazidulalam47) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External BDJobs users and agents supporting them use this skill to configure a job profile, search and rank fresh jobs, apply to selected matches, cancel applications, and update expected salary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores BDJobs passwords, reusable session tokens, and resume data locally. <br>
Mitigation: Treat the data folder and command output as sensitive, restrict access to the workspace, and delete stored credentials or tokens when they are no longer needed. <br>
Risk: The skill can apply to jobs, cancel applications, and update salary expectations on a live BDJobs account. <br>
Mitigation: Require explicit user confirmation before apply, undo, or salary-update actions and review proposed job matches before execution. <br>


## Reference(s): <br>
- [BDJobs API Reference](references/api.md) <br>
- [ClawHub Release Page](https://clawhub.ai/sazidulalam47/bdjobs-job-apply) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration files and shell command execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local data files for credentials, session data, resume content, job lists, application results, and salary updates.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
