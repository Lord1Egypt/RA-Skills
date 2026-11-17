## Description:

ClamAV open-source antivirus reference. clamscan, freshclam database updates, clamd daemon configuration, custom signatures, quarantine workflows, automated scanning, and performance tuning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, system administrators, and security engineers use this skill as a ClamAV reference for scanning, database updates, daemon configuration, custom signatures, quarantine workflows, automation, and performance tuning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes permissive clamd socket guidance such as LocalSocketMode 666.

Mitigation: Use least-privilege socket permissions and group-based access, and avoid world-writable local sockets unless a host-specific review approves them.

Risk: The artifact includes package installation, service enablement, cron, and full-system scan examples that can alter host behavior or affect production workloads.

Mitigation: Review commands for the target host, test in an isolated environment, and scope scans and schedules to approved paths and maintenance windows.

Risk: The artifact includes quarantine cleanup and removal examples that can permanently delete files.

Mitigation: Prefer copy or move quarantine workflows first, preserve logs and evidence, and delete only after explicit verification and retention review.

Risk: The artifact references cvdupdate for local mirror workflows.

Mitigation: Pin, isolate, and review cvdupdate before use, and run mirror components with restricted permissions.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)
- [ClamAV 1.3.0 source archive](https://www.clamav.net/downloads/production/clamav-1.3.0.tar.gz)
- [EICAR test file](https://secure.eicar.org/eicar.com.txt)
- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/clamav)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reference text with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands can affect system services, socket permissions, scan scope, quarantine behavior, or file deletion and should be reviewed before operational use.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
