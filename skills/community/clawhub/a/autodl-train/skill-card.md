## Description: <br>
Operates remote model training jobs on AutoDL Linux servers over SSH for launching runs, checking status, monitoring resources, reading logs, diagnosing interruptions, and summarizing outcomes with next-step recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zhuoran-Liu](https://clawhub.ai/user/Zhuoran-Liu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML engineers use this skill to operate AutoDL training runs over SSH, including launch, resume, health checks, resource monitoring, log review, failure diagnosis, and run summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires SSH access to an AutoDL server and can use sensitive connection details. <br>
Mitigation: Review config.json and any .env file before use, prefer SSH keys, and use a least-privileged remote account where possible. <br>
Risk: Launched training jobs can continue consuming GPU time, disk, and cloud credits. <br>
Mitigation: Monitor launched jobs with the bundled status, resource, and log summary scripts. <br>
Risk: Incorrect host, project path, training command, log path, or resume arguments can affect the wrong environment or produce misleading diagnostics. <br>
Mitigation: Confirm host, username, project_path, ssh_key_path, train_command, log_path, and resume arguments before running commands. <br>


## Reference(s): <br>
- [Usage Guide](references/usage.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Zhuoran-Liu/autodl-train) <br>
- [Publisher Profile](https://clawhub.ai/user/Zhuoran-Liu) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Text, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise status or diagnostic summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference JSON output from bundled scripts when the user requests structured status, resource, or log summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
