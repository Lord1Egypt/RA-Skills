## Description: <br>
通过 WebSocket 控制真实浏览器，实现导航、点击、输入、截图、DOM 获取等完整自动化操作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linbo405](https://clawhub.ai/user/linbo405) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to let an agent drive a local Chromium browser over WebSocket for navigation, clicking, typing, screenshots, DOM snapshots, and status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes powerful unauthenticated control over a real browser through local WebSocket and DevTools ports. <br>
Mitigation: Run it only on a trusted machine, keep the ports inaccessible from other systems, stop the service when finished, and review commands before use. <br>
Risk: Browser automation can act on authenticated websites or profiles with sensitive sessions. <br>
Mitigation: Use a separate browser profile with no sensitive logins and avoid authenticated sites unless the automation is explicitly intended to act there. <br>
Risk: The artifact includes a site-specific helper for Fanqie that may be unrelated to general browser-control use. <br>
Mitigation: Review, remove, or ignore quick-control.js when that workflow is outside the intended deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linbo405/ai-browser-ws) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON, JavaScript, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce WebSocket command payloads and browser automation guidance; screenshots are returned by the running service as base64 data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
