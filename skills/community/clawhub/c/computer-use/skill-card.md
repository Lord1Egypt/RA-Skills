## Description: <br>
Full desktop computer use for headless Linux servers. Xvfb + XFCE virtual desktop with xdotool automation. 17 actions (click, type, scroll, screenshot, drag, etc). Unlike OpenClaw's browser tool, operates at the X11 level so websites cannot detect automation. Includes VNC for live viewing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ram-Raghav-S](https://clawhub.ai/user/Ram-Raghav-S) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to set up and control a headless Linux desktop through Xvfb, XFCE, xdotool, screenshots, and optional VNC viewing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup installs persistent remote-desktop services and makes broad system changes. <br>
Mitigation: Run it only on a dedicated disposable headless server or VM, inspect setup-vnc.sh first, and prepare rollback steps for disabling services and restoring /usr/bin/xfdesktop. <br>
Risk: VNC and noVNC access can expose interactive desktop control if ports are reachable by untrusted networks. <br>
Mitigation: Restrict VNC/noVNC to localhost or firewall-only access, add authentication, and avoid publicly exposing ports 5900 or 6080. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Ram-Raghav-S/computer-use) <br>
- [Google Chrome Linux Package](https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and command output such as base64 PNG screenshots] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a 1024x768 X11 display on :99 and may return screenshots after desktop actions.] <br>

## Skill Version(s): <br>
1.2.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
