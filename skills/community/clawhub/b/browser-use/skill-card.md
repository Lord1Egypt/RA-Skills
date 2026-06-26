## Description: <br>
Automates browser interactions for web testing, form filling, screenshots, and data extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnpana](https://clawhub.ai/user/shawnpana) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to drive browser sessions for web testing, form entry, screenshots, authenticated browsing, and page data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad access to logged-in browser sessions, cookies, cloud profile syncing, public tunnels, and raw browser internals. <br>
Mitigation: Use isolated or throwaway browser profiles, avoid syncing profiles to cloud unless intended, do not export or print cookies unless explicitly handling session secrets, and close browser sessions plus tunnels when finished. <br>
Risk: Browser automation can perform file uploads, account changes, or other actions with real user impact. <br>
Mitigation: Confirm any file upload, credential use, account-changing action, or public tunnel exposure before executing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shawnpana/browser-use) <br>
- [CDP Python reference](references/cdp-python.md) <br>
- [Multi-session reference](references/multi-session.md) <br>
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text, Code] <br>
**Output Format:** [Markdown with inline shell commands and browser automation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce screenshots, extracted page text, HTML, JSON command output, cookie exports, and configuration instructions through the browser-use CLI.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
