## Description: <br>
Scheduled task and cron job anti-pattern analyzer that detects overlapping execution risks, timezone scheduling errors, missing error recovery, resource contention, lifecycle management issues, and observability gaps in cron jobs, schedulers, and periodic task code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use cronlint to scan repositories for cron job and scheduled task anti-patterns, review findings with remediation guidance, and produce text, JSON, HTML, or markdown reports for local review or CI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CronLint reads the target repository during local scans. <br>
Mitigation: Run it only on repositories you intend to inspect, use explicit paths, and review findings before relying on them. <br>
Risk: Paid tiers use a license key and license token handling was flagged for review. <br>
Mitigation: Avoid passing license keys on the command line, store keys only in trusted environment or configuration locations, and do not use untrusted license tokens. <br>
Risk: Optional git hook installation can add persistent commit and push scanning to a repository. <br>
Mitigation: Install hooks only in repositories where ongoing CronLint checks are desired and review the hook configuration before committing it. <br>


## Reference(s): <br>
- [CronLint homepage](https://cronlint.pages.dev) <br>
- [CronLint hook documentation](https://cronlint.pages.dev/docs/hooks) <br>
- [ClawHub cronlint listing](https://clawhub.ai/suhteevah/cronlint) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML, shell commands, guidance] <br>
**Output Format:** [CLI output and reports in text, JSON, HTML, or markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally against selected files or directories and may return nonzero exit codes when scheduling quality falls below the configured threshold.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
