## Description: <br>
Control a Mac through natural language - open apps, click buttons, read the screen, type text, manage windows, and automate multi-step tasks via Airpoint's AI computer-use agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarioAndF](https://clawhub.ai/user/MarioAndF) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and end users on macOS use this skill to ask Airpoint's CLI agent to inspect the current screen, control apps, type, click, manage windows, and automate multi-step desktop tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Airpoint can read the screen and control keyboard and mouse input on macOS, which can expose sensitive information or perform unintended actions. <br>
Mitigation: Use the skill only for narrow supervised tasks, avoid private messages, secrets, financial or account actions, review results and screenshots, and revoke macOS Accessibility or Screen Recording permissions when not needed. <br>
Risk: Fire-and-forget execution can let a task continue without direct observation. <br>
Mitigation: Prefer the default waiting mode over `--no-wait`, and use `airpoint stop` to cancel tasks that are stuck or behaving unexpectedly. <br>


## Reference(s): <br>
- [Airpoint homepage](https://airpoint.app) <br>
- [ClawHub Airpoint release](https://clawhub.ai/MarioAndF/airpoint) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The Airpoint CLI may return text summaries and screenshot file paths for visual confirmation.] <br>

## Skill Version(s): <br>
1.3.16 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
