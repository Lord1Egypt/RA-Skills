## Description: <br>
Slash OpenClaw token costs and prevent context overflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omaression](https://clawhub.ai/user/omaression) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose high OpenClaw token usage, context overflow, noisy memory retrieval, and long-session slowdown, then apply focused configuration changes or run the bundled optimizer script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aggressive defaults and broad activation triggers can change OpenClaw behavior in more situations than expected. <br>
Mitigation: Review proposed config changes and scripts before applying them, treat aggressive settings as reversible recommendations, and loosen settings if task quality drops. <br>


## Reference(s): <br>
- [Aggressive all-in-one config](references/aggressive-config.md) <br>
- [Commands cheat sheet](references/commands.md) <br>
- [Config examples](references/configs.md) <br>
- [ClawHub release page](https://clawhub.ai/omaression/aggressive-context-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose balanced or aggressive OpenClaw configuration changes and validation commands.] <br>

## Skill Version(s): <br>
1.0.0-alpha (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
