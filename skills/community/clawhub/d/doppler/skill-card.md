## Description: <br>
Manage secrets and environment variables via the Doppler CLI for secrets, projects, configs, environments, setup, authentication, and activity review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Melvynx](https://clawhub.ai/user/Melvynx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to ask an agent for Doppler CLI command guidance when configuring projects, managing secrets and environments, running commands with injected secrets, and reviewing Doppler activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward commands that expose plaintext secrets. <br>
Mitigation: Require explicit user intent before retrieving or downloading secrets, redact command output, and avoid printing plaintext values unless strictly necessary. <br>
Risk: The skill includes destructive commands for deleting secrets, projects, configs, and environments. <br>
Mitigation: Confirm the exact project, config, environment, and secret key before destructive operations and require explicit confirmation for deletes. <br>
Risk: Downloaded secret sets can persist sensitive data on disk. <br>
Mitigation: Avoid saving downloaded secrets to disk unless controlled storage and cleanup are in place. <br>


## Reference(s): <br>
- [Doppler CLI installation documentation](https://docs.doppler.com/docs/install-cli) <br>
- [ClawHub Doppler skill page](https://clawhub.ai/Melvynx/doppler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command guidance should prefer JSON output for programmatic calls and should redact plaintext secret values.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
