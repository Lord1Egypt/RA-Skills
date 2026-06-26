## Description: <br>
OpenClaw Gateway Resilience Guard helps keep OpenClaw Gateway, channels, diagnostics, logs, and optional model-provider probes observable after network changes, sleep or resume events, session expiry, provider timeouts, or partial outages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zc-kama](https://clawhub.ai/user/zc-kama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who run OpenClaw continuously use this skill to install and operate a local watchdog for Gateway, channel, network, diagnostic, and optional model-provider health. The skill provides guarded recovery workflows, dashboard access, service management commands, and configuration guidance for Linux, WSL, macOS, and Windows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a persistent local watchdog that can restart OpenClaw Gateway and expose a localhost dashboard. <br>
Mitigation: Install with no auto-start first when reviewing, inspect the generated watchdog configuration, and enable dashboard actions only when the operator needs local control. <br>
Risk: Dashboard actions and restart paths can execute local commands when explicitly enabled or configured. <br>
Mitigation: Keep diagnostic and model-probe actions in log-only mode unless the configuration file is controlled and reviewed; avoid custom command actions for untrusted configurations. <br>
Risk: The optional model-provider probe sends real OpenClaw model requests and may consume provider quota or cost. <br>
Mitigation: Leave model probing disabled by default; when enabled, use the documented low-volume diagnostic settings and keep the action set to log. <br>
Risk: Diagnostic logs and exports may include local paths, service names, channel URLs, provider or model names, timing, exit status, and error snippets. <br>
Mitigation: Review logs and exported diagnostic bundles before sharing them outside the local operator environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zc-kama/gateway-resilience-guard) <br>
- [README.md](README.md) <br>
- [Tencent/openclaw-weixin issue 141](https://github.com/Tencent/openclaw-weixin/issues/141) <br>
- [Tencent/openclaw-weixin issue 155](https://github.com/Tencent/openclaw-weixin/issues/155) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code] <br>
**Output Format:** [Markdown with shell and PowerShell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes install, dashboard, service-management, diagnostic, and safety guidance for a local OpenClaw watchdog.] <br>

## Skill Version(s): <br>
1.4.4 (source: server release, CHANGELOG.md, package.json, OpenClaw plugin manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
