## Description: <br>
CLI tool to clean up stopped Docker containers, unused images, volumes, and networks to free up disk space. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Derick001](https://clawhub.ai/user/Derick001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to inspect Docker resource usage and remove stopped containers, unused images, volumes, and networks to reclaim disk space. It supports interactive cleanup, dry runs, and script-friendly status output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Docker cleanup operations can delete containers, images, volumes, or networks, and the security review warns the implementation may delete resources without the documented confirmation. <br>
Mitigation: Use only on non-production Docker hosts or after backups, run --dry-run first, and do not rely on interactive confirmation unless the implementation is fixed. <br>
Risk: Docker access may require elevated host privileges and can affect host resources beyond the current project. <br>
Mitigation: Run with the least necessary Docker permissions, inspect target resources before cleanup, and avoid --force or --yes unless the target host is disposable or backed up. <br>


## Reference(s): <br>
- [Docker Container Cleaner README](artifact/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/Derick001/docker-container-cleaner) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI output can be human-readable text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and docker binaries; destructive cleanup modes should be previewed with dry-run first.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
