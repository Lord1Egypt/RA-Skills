## Description: <br>
Guides developers through using Claude Code with OpenClaw for coding, debugging, refactoring, and PR review via ACP or PTY workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xwz119](https://clawhub.ai/user/xwz119) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure OpenClaw to delegate coding tasks to Claude Code, manage ACP or PTY sessions, and apply cost-control practices for coding workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can grant broad unattended coding permissions that may modify project files without enough user checkpoints. <br>
Mitigation: Use a sandbox or disposable branch, keep the working directory narrow, prefer explicit approval modes, and avoid approve-all for normal use. <br>
Risk: Persistent or background sessions may continue working after the user stops actively monitoring them. <br>
Mitigation: Monitor session logs, cancel or close sessions when finished, and add explicit completion or wake-up commands for long-running tasks. <br>
Risk: API keys and model usage can create credential exposure or unexpected spend. <br>
Mitigation: Protect API keys, set provider spending limits, and use per-task budget caps where supported. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xwz119/claude-code-dev) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with shell commands, JSON examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational guidance for ACP sessions, PTY execution, API key setup, model selection, and budget controls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
