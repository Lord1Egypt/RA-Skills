## Description: <br>
Real-time companion monitor for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luccast](https://clawhub.ai/user/luccast) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Crabwalk to install and run a real-time monitor for OpenClaw agent activity, workspace browsing, and human review over a local or LAN-accessible web interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installation flow downloads and runs an unpinned remote release binary. <br>
Mitigation: Use a pinned and verified release before execution, and review commands before running package-manager or sudo steps. <br>
Risk: The monitor may expose agent activity, workspace files, and OpenClaw gateway-backed access to anyone who can reach the server. <br>
Mitigation: Bind to localhost unless LAN sharing is required, share access only with trusted users, and avoid exposing the server beyond the local network. <br>
Risk: The tool can read OpenClaw credentials from local configuration. <br>
Mitigation: Run it only when the Crabwalk publisher and release are trusted, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luccast/crabwalk) <br>
- [Crabwalk homepage](https://crabwalk.app) <br>
- [Crabwalk feedback skill](https://crabwalk.app/feedback-skill) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides installation, verification, startup, update prompts, and feedback capture for the Crabwalk monitor.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
