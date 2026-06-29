## Description: <br>
Drift detection + baseline integrity guard for agent workspace files with automatic alerting support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor OpenClaw agent workspace files for unexpected drift, review patch evidence, and optionally restore protected prompt or instruction files to an approved baseline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restore mode can overwrite protected workspace files. <br>
Mitigation: Start with read-only or dry-run checks, review drift output, and require explicit approval before enabling restore actions. <br>
Risk: Optional cron or launchd scheduling can create persistent workspace monitoring. <br>
Mitigation: Inspect generated schedule, LaunchAgent label, script path, and state directory before enabling any background job. <br>
Risk: Local state may contain approved snapshots, diffs, and quarantine copies of sensitive workspace files. <br>
Mitigation: Use a dedicated external state directory with restrictive permissions and avoid using the skill on sensitive workspaces unless local copies are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davida-ps/skills/clawsec-openclaw-soul-guardian) <br>
- [Project homepage](https://clawsec.prompt.security) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Text] <br>
**Output Format:** [Markdown guidance with shell commands and local status or alert text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local audit, patch, baseline, and quarantine files when its scripts are run.] <br>

## Skill Version(s): <br>
0.0.9 (source: frontmatter, release evidence, changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
