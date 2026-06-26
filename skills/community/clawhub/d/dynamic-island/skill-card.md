## Description: <br>
macOS Dynamic Island desktop widget for OpenClaw that shows real-time multi-agent status, recent messages, and state changes in a frosted glass pill UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhixiangshon-cell](https://clawhub.ai/user/zhixiangshon-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to monitor multiple local OpenClaw agents from a macOS desktop widget, including status, recent messages, completion signals, and optional Feishu or Lark chat links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The widget reads local OpenClaw session files and may display recent conversation snippets. <br>
Mitigation: Use only on a trusted Mac and avoid exposing sensitive agent sessions to untrusted local users or processes. <br>
Risk: Local HTTP and WebSocket access controls are weak for data that can include recent agent messages. <br>
Mitigation: Prefer a version with a local auth token or Origin checks before deploying beyond a single trusted workstation. <br>
Risk: Displayed message or configuration text could include unsafe or unexpected content. <br>
Mitigation: Escape displayed message and configuration text before rendering it in the widget UI. <br>
Risk: Configured chat links can open external app URLs. <br>
Mitigation: Limit configured links to expected Feishu or Lark schemes and review config.json before use. <br>
Risk: The optional login-start setup can make the widget run automatically. <br>
Mitigation: Clearly label LaunchAgent setup as optional and install it only when persistent startup is intended. <br>


## Reference(s): <br>
- [Dynamic Island ClawHub page](https://clawhub.ai/zhixiangshon-cell/dynamic-island) <br>
- [OpenClaw project](https://github.com/nicepkg/openclaw) <br>
- [emolog App Store page](https://apps.apple.com/app/emolog/id6443809191) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup, start, stop, and configuration guidance for a macOS OpenClaw status widget.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; skill frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
