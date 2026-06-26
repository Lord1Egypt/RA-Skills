## Description: <br>
Recover from developer disasters. Use when someone force-pushed to main, leaked credentials in git, ran out of disk space, killed the wrong process, corrupted a database, broke a deploy, locked themselves out of SSH, lost commits after a bad rebase, or hit any other "oh no" moment that needs immediate, calm, step-by-step recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill during urgent operational failures to diagnose the situation, choose recovery commands, and verify that the fix worked. It covers git history incidents, leaked credentials, disk pressure, stuck processes, database failures, deploy rollbacks, access lockouts, SSL expiration, and network failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recovery commands can affect shared repositories, production hosts, databases, credentials, and deployments if applied to the wrong target. <br>
Mitigation: Confirm the exact repository, branch, account, database, host, and production impact before running any command. <br>
Risk: Some procedures include destructive or hard-to-reverse operations such as force pushes, hard resets, Docker pruning with volumes, database termination, sudo changes, cron edits, and credential revocation. <br>
Mitigation: Require explicit human approval for destructive steps, coordinate with teammates for shared systems, and make backups where feasible. <br>
Risk: The skill is a transparent emergency runbook, but following incorrect guidance during an incident can worsen downtime or data loss. <br>
Mitigation: Use the diagnose, fix, verify sequence and review each proposed command before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gitgoodordietrying/emergency-rescue) <br>
- [Publisher profile](https://clawhub.ai/user/gitgoodordietrying) <br>
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are presented as human-reviewed recovery procedures rather than hidden execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
