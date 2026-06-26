## Description: <br>
Manages Clash/mihomo proxy environments, including installation, proxy startup and shutdown, subscription management, web panel operations, Tun mode configuration, and kernel upgrades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kklldog](https://clawhub.ai/user/kklldog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to administer local Clash/mihomo proxy environments through command-line guidance for installation, subscriptions, system proxy settings, web panel access, Tun mode, upgrades, and uninstall steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide system-wide networking changes for Clash/mihomo proxy operation. <br>
Mitigation: Confirm each command before execution, verify the installer source, and keep a rollback path for disabling proxy settings. <br>
Risk: Web panel access or Tun mode can broaden local network exposure or require elevated privileges. <br>
Mitigation: Restrict panel access, rotate or reset the panel secret when exposed, prefer SSH forwarding for remote access, and know how to disable Tun mode. <br>


## Reference(s): <br>
- [Clash Controller on ClawHub](https://clawhub.ai/kklldog/clash-controller) <br>
- [clash-for-linux-install installer referenced by the skill](https://gh-proxy.org/https://github.com/nelvko/clash-for-linux-install.git) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command guidance can affect local networking, proxy settings, web panel exposure, and Tun mode configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
