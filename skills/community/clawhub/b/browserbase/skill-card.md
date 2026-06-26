## Description: <br>
Create and manage persistent Browserbase cloud browser sessions with authentication persistence, captcha solving, session recording, screenshots, browser automation, and session cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JamesFincher](https://clawhub.ai/user/JamesFincher) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to create and manage Browserbase cloud browser sessions for authenticated browsing, research capture, screenshot generation, and controlled browser automation across persistent contexts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control logged-in Browserbase sessions and persist authentication state across contexts. <br>
Mitigation: Use separate contexts per site, terminate sessions promptly, and delete contexts when the work is finished. <br>
Risk: Commands can read cookies and execute JavaScript in authenticated browser sessions. <br>
Mitigation: Use get-cookies and execute-js only when explicitly needed, with trusted target pages and reviewed JavaScript. <br>
Risk: Session recording, logs, and CAPTCHA solving are enabled or available for workflows that may involve sensitive sites. <br>
Mitigation: Disable recording and CAPTCHA solving for sensitive workflows, avoid unnecessary log collection, and review captured artifacts before sharing. <br>
Risk: Dependencies are declared with minimum versions rather than pinned exact versions. <br>
Mitigation: Install in an isolated environment and consider pinning dependency versions for repeatable deployments. <br>


## Reference(s): <br>
- [Browserbase API Quick Reference](references/api-quick-ref.md) <br>
- [Browserbase](https://www.browserbase.com/) <br>
- [Browserbase API](https://api.browserbase.com/v1) <br>
- [ClawHub Skill Page](https://clawhub.ai/JamesFincher/browserbase) <br>
- [Publisher Profile](https://clawhub.ai/user/JamesFincher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output from the manager script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create Browserbase sessions, screenshots, recordings, logs, cookies, and local context-name configuration files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
