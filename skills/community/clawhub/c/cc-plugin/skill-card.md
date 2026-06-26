## Description: <br>
Claude Code plugin lifecycle management for creating, maintaining, troubleshooting, and locally testing plugins and marketplaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to manage Claude Code plugin authoring, marketplace operations, cache cleanup, local plugin reflection, HUD configuration, and troubleshooting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide edits to local Claude Code plugin settings, cache directories, and marketplace clones. <br>
Mitigation: Use documented dry-run paths where available, review target paths before execution, and back up ~/.claude/settings.json before enabling plugins. <br>
Risk: Cache cleanup and reflection workflows may remove or overwrite local plugin cache or marketplace clone content. <br>
Mitigation: Treat marketplace clone edits as disposable test changes, verify source and destination paths, and keep durable changes in the source repository. <br>
Risk: Troubleshooting guidance may include npm install/build steps for plugin code. <br>
Mitigation: Run build or install commands only for plugin sources you trust and inspect package scripts before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drumrobot/cc-plugin) <br>
- [Cache cleanup guide](cache.md) <br>
- [Plugin creation guide](create.md) <br>
- [Dev reflect guide](dev-reflect.md) <br>
- [HUD configuration guide](hud.md) <br>
- [Marketplace management guide](marketplace.md) <br>
- [Plugin troubleshooting guide](troubleshoot.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON snippets, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional helper script invocations and dry-run flows for local plugin management.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata and CHANGELOG, released 2026-06-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
