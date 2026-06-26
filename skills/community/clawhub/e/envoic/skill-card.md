## Description: <br>
Scan, audit, and clean up Python virtual environments, conda environments, node_modules directories, and development artifacts that consume disk space. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mahimairaja](https://clawhub.ai/user/mahimairaja) <br>

### License/Terms of Use: <br>
BSD-3-Clause <br>


## Use Case: <br>
Developers and engineers use this skill to audit workspace disk usage, identify stale or broken Python and JavaScript environments, and prepare safe cleanup plans before deleting generated artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup commands can delete development environments or generated artifacts if run against the wrong path or without review. <br>
Mitigation: Start with a narrow folder, scan first, run dry-runs before deletion, inspect proposed deletions, and require explicit confirmation for non-dry-run cleanup. <br>
Risk: Using automatic yes flags or remote install scripts can bypass review of actions or source trust. <br>
Mitigation: Avoid --yes unless the listed items are safe to recreate, and do not pipe remote install scripts into a shell unless the source has been trusted and verified. <br>


## Reference(s): <br>
- [envoic Commands Reference](references/commands.md) <br>
- [envoic Safety Guide](references/safety.md) <br>
- [envoic Troubleshooting](references/troubleshooting.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mahimairaja/envoic) <br>
- [Repository](https://github.com/mahimailabs/envoic) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON report commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cleanup guidance should start with scan and dry-run steps, require explicit confirmation before deletion, and preserve lock files and project manifests.] <br>

## Skill Version(s): <br>
0.0.9 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
