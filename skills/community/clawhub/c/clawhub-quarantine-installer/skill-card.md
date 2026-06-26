## Description: <br>
Installs and audits ClawHub skills in an isolated quarantine directory for security review before production use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alessandropcostabr](https://clawhub.ai/user/alessandropcostabr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to install a selected ClawHub skill into a quarantine directory, run basic pattern-based auditing, and decide whether to promote it manually. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can force-install ClawHub skills that are already flagged as suspicious, which may introduce untrusted code into the runtime environment. <br>
Mitigation: Run it only in a disposable workspace, container, or VM with no valuable credentials or personal files, as directed by the security guidance. <br>
Risk: The quarantine directory limits where the target skill is installed but does not provide complete containment. <br>
Mitigation: Review the exact target skill and avoid using this workflow on a normal OpenClaw profile unless persistent skill-environment changes are acceptable. <br>
Risk: The audit is pattern-based and may miss risky behavior that does not match the searched patterns. <br>
Mitigation: Treat the generated report as a starting point and perform manual source and dependency review before promoting any quarantined skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alessandropcostabr/clawhub-quarantine-installer) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Files, Guidance] <br>
**Output Format:** [Terminal output and plain-text audit reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes quarantine installations and timestamped audit reports under $HOME/.openclaw/clawhub-quarantine when the scripts are run.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
