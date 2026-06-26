## Description: <br>
Corveil starts a local Corveil dev gateway and configures OpenClaw or Claude Code to route AI requests through it for logging, guardrails, spend tracking, and direct or passthrough provider access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dgershman](https://clawhub.ai/user/dgershman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to set up a local Corveil development environment and connect OpenClaw or Claude Code for testing AI request capture, guardrails, spend tracking, plugins, and direct or passthrough provider routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Corveil observes and logs routed AI requests, which can include sensitive prompts, responses, or development context. <br>
Mitigation: Install only when request logging is intended, avoid routing production secrets through dev mode, and review captured data handling before use. <br>
Risk: Provider credentials are used for passthrough or direct routing during local setup. <br>
Mitigation: Use dev or test provider keys, rotate them after testing when appropriate, and keep the original OpenClaw or Claude Code settings so routing can be reverted. <br>
Risk: The workflow installs or runs Corveil binaries or installer scripts from external release locations. <br>
Mitigation: Verify downloaded binaries or installer scripts before running them, including published checksums where available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dgershman/corveil) <br>
- [Corveil documentation](https://corveil.com/docs) <br>
- [Corveil GitHub Releases](https://github.com/radiusmethod/corveil-releases/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local setup commands, environment variables, OpenClaw provider configuration, and verification steps.] <br>

## Skill Version(s): <br>
1.0.6-20260516 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
