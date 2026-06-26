## Description: <br>
Browser Agent lets an agent control a local Chrome browser through Chrome DevTools Protocol for navigation, screenshots, clicks, typing, JavaScript evaluation, session reuse, data collection, content management, and browser-based testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaka4413](https://clawhub.ai/user/kaka4413) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to connect agents to Chrome CDP, reuse browser sessions, and automate browser workflows such as web data collection, form interactions, content publishing, cross-platform synchronization, screenshots, and UI regression checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over real logged-in Chrome sessions. <br>
Mitigation: Use a separate Chrome profile with non-sensitive accounts and require explicit confirmation before posting, deleting, submitting forms, or other state-changing actions. <br>
Risk: Chrome CDP access can expose powerful browser control if the debugging endpoint is reachable beyond the intended local session. <br>
Mitigation: Keep CDP bound to localhost and avoid wildcard remote origins when possible. <br>
Risk: Browser automation and JavaScript evaluation can be unsafe on sensitive sites. <br>
Mitigation: Avoid using the skill on banking, email, admin consoles, password managers, or other sensitive sites unless reviewed and explicitly approved. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/kaka4413/browser-agent) <br>
- [Browser Agent API Reference](references/api_reference.md) <br>
- [Chrome DevTools Protocol Documentation](https://chromedevtools.github.io/devtools-protocol/) <br>
- [websocket-client Documentation](https://websocket-client.readthedocs.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets, CLI status text, and generated browser artifacts such as screenshots when actions are executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime behavior depends on access to a local Chrome CDP endpoint and may act on logged-in browser sessions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
