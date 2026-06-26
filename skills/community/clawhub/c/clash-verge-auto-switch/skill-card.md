## Description: <br>
Use when the user wants Codex to speed test Clash Verge Rev or Mihomo proxies, auto-detect currently used Clash groups from the live controller, switch a selector group to the fastest working node, diagnose controller connectivity, or install a macOS launchd job with a user-chosen interval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tankeito](https://clawhub.ai/user/tankeito) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let Codex inspect a local Clash Verge Rev or Mihomo controller, test proxy latency, switch selected groups to the fastest healthy node, and set up or remove a macOS launchd schedule for repeated switching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change local Clash/Mihomo selector choices through the controller API. <br>
Mitigation: Start with --dry-run or --list-groups, target explicit groups when needed, and confirm the reported winning node before allowing changes. <br>
Risk: Controller secrets or remote controller URLs can expose proxy control beyond the intended local session. <br>
Mitigation: Keep the controller local or otherwise trusted, protect any controller secret, and avoid sharing logs or commands that include secret values. <br>
Risk: The launchd installer creates a recurring user-level schedule that continues switching proxies until removed. <br>
Mitigation: Choose the interval deliberately, review the generated job behavior through the install output and logs, and run the bundled uninstall script when scheduled switching is no longer wanted. <br>


## Reference(s): <br>
- [Runtime Notes](artifact/references/runtime-notes.md) <br>
- [ClawHub Release Page](https://clawhub.ai/tankeito/clash-verge-auto-switch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and execution summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke bundled Python and shell scripts that read local Clash/Mihomo controller settings, call the local controller API, and optionally install a user-level macOS launchd job.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
