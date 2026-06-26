## Description: <br>
Safely inject API keys from 1Password into macOS LaunchAgent plists using PlistBuddy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to populate OpenClaw gateway LaunchAgent environment variables on macOS from secrets stored in 1Password. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists provider API keys and a 1Password service account token into a local LaunchAgent plist. <br>
Mitigation: Review the script before use, use tightly scoped and rotatable credentials, inspect plist permissions, and remove OP_SERVICE_ACCOUNT_TOKEN unless the gateway truly needs it. <br>
Risk: Old secrets can remain in the LaunchAgent plist after key rotation or configuration changes. <br>
Mitigation: Plan cleanup for stale values in the plist and verify the resulting EnvironmentVariables block after each run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/gateway-env-injector) <br>
- [Publisher profile](https://clawhub.ai/user/nissan) <br>
- [1Password](https://1password.com) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples and a shell script artifact] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, the 1Password CLI, and OP_SERVICE_ACCOUNT_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
