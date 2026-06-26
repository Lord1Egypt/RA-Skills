## Description: <br>
Installs, updates, runs, and verifies the public ClawStatus dashboard locally or on a LAN host. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NeverChenX](https://clawhub.ai/user/NeverChenX) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to deploy or refresh ClawStatus, restart the dashboard service, and verify that the dashboard is reachable on port 8900. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer clones and installs code from a GitHub repository. <br>
Mitigation: Install only when the target repository is trusted, and prefer a virtual environment or dedicated user account. <br>
Risk: Overriding REPO_URL can redirect installation to a different repository. <br>
Mitigation: Avoid overriding REPO_URL unless the replacement repository is trusted. <br>
Risk: Binding the dashboard to 0.0.0.0 can expose it to LAN devices. <br>
Mitigation: Bind to 127.0.0.1 unless LAN access is intentionally required. <br>


## Reference(s): <br>
- [ClawStatus command reference](references/commands.md) <br>
- [ClawHub skill page](https://clawhub.ai/NeverChenX/clawstatus-dashboard) <br>
- [ClawStatus GitHub repository install target](https://github.com/NeverChenX/ClawStatus.git) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes install/update, foreground run, systemd user service, and HTTP verification commands.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
