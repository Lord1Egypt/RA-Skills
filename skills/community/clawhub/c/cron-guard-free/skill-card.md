## Description: <br>
Cron Guard Free helps agents harden cron jobs with script-first execution guidance, common failure-mode diagnosis, basic guardrails, and recovery patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, operations engineers, and system administrators use this skill to design safer cron workflows, diagnose scheduled-task failures, and add timeout, exit-code, logging, alerting, retry, skip, and degrade patterns to local scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to run local scripts, which may affect files, services, or scheduled jobs if used on untrusted paths or production systems. <br>
Mitigation: Review each script before execution, run only user-selected trusted scripts, prefer dry-run or non-production testing first, and avoid writable or untrusted paths. <br>
Risk: Logging and alert examples write local files and could create unexpected artifacts outside intended locations. <br>
Mitigation: Keep log and alert paths constrained to expected directories and verify permissions before using the examples. <br>


## Reference(s): <br>
- [Detailed cron guard examples](references/detail.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local script execution patterns, logging paths, health checks, and recovery strategies for user-selected cron jobs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
