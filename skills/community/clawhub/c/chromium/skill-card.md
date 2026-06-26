## Description: <br>
Launches a persistent headless Chromium session with Chrome DevTools Protocol access for browser automation, screenshots, and cookie import. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redf426](https://clawhub.ai/user/redf426) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to give OpenClaw agents a persistent headless browser for navigation, page inspection, clicks, form filling, screenshots, and authenticated browsing via imported cookies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent browser profiles and imported cookies can expose authenticated sessions. <br>
Mitigation: Use an isolated machine or container, avoid importing valuable account cookies, delete cookie export files after import, and clear the browser profile when finished. <br>
Risk: The supplied launcher disables Chromium sandboxing. <br>
Mitigation: Run Chromium on a least-privileged isolated host or container and avoid combining unsandboxed browsing with sensitive accounts or files. <br>
Risk: Remote debugging enables browser control through the local CDP endpoint. <br>
Mitigation: Keep the endpoint bound to 127.0.0.1, do not forward the debug port, and close Chromium when browser automation is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Chromium Skill](https://clawhub.ai/redf426/chromium) <br>
- [Cookie-Editor](https://cookie-editor.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and browser-control instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist browser profile state and imported cookies; uses a local CDP endpoint for browser automation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
