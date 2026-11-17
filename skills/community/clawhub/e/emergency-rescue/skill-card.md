## Description:

Recover from developer disasters. Use when someone force-pushed to main, leaked credentials in git, ran out of disk space, killed the wrong process, corrupted a database, broke a deploy, locked themselves out of SSH, lost commits after a bad rebase, or hit any other "oh no" moment that needs immediate, calm, step-by-step recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill as an emergency recovery runbook for git mistakes, credential leaks, disk pressure, process failures, database incidents, deployment rollbacks, access lockouts, certificate issues, and network failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recovery commands may delete data, kill services, rewrite shared history, prune Docker resources, or install recurring jobs if copied without review.

Mitigation: Review each command before execution and confirm the target repository, branch, process, Docker resource, filesystem path, crontab entry, and available backup.

Risk: Credential-recovery steps may expose or mishandle secrets if live values are pasted into terminals, logs, or shared channels.

Mitigation: Revoke or rotate exposed credentials first, avoid pasting live secrets into command history, and verify cleanup without disclosing secret values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gitgoodordietrying/skills/emergency-rescue)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Procedural recovery guidance organized as diagnose, fix, and verify steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
