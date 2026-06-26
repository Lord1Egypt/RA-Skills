## Description: <br>
Claw Insights Install guides agents through installing, running, configuring, upgrading, and troubleshooting Claw Insights, a local read-only observability dashboard for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LucaL6](https://clawhub.ai/user/LucaL6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up and operate a local Claw Insights dashboard for OpenClaw observability, including installation, service management, authentication, configuration, upgrades, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends running a remote installer, which can execute code from claw-insights.com on the user's machine. <br>
Mitigation: Install only if the publisher and installer are trusted, inspect the installer before execution, or use the npm package path when that better fits local review controls. <br>
Risk: The dashboard can surface local agent transcripts and tool activity. <br>
Mitigation: Keep authentication enabled, bind the service to localhost, and review database and retention settings before use. <br>
Risk: Disabling authentication can expose transcript and activity data to anyone who can reach the service. <br>
Mitigation: Avoid `--no-auth` except in controlled local environments, and do not expose the service directly to the internet without authentication. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/LucaL6/claw-insights-install) <br>
- [Configuration Reference](references/configuration.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Claw Insights installer](https://claw-insights.com/install.sh) <br>
- [Node.js](https://nodejs.org) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks and configuration tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local service commands, environment variable guidance, verification steps, and troubleshooting checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
