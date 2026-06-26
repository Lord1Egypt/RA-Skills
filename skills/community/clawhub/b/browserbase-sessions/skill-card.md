## Description: <br>
Create and manage persistent Browserbase cloud browser sessions with authentication persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JamesFincher](https://clawhub.ai/user/JamesFincher) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation engineers use this skill to create, resume, inspect, and terminate Browserbase cloud browser sessions for authenticated browsing, browser automation, screenshots, recordings, logs, downloads, and human handoff workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control cloud browsers that may remain logged into websites and preserve cookies or local storage. <br>
Mitigation: Use a dedicated Browserbase project and API key, isolate workspaces per site or task, avoid exporting cookies, terminate sessions, and delete contexts when work is finished. <br>
Risk: Session recording, logging, and CAPTCHA solving are enabled by default and can capture sensitive browsing activity. <br>
Mitigation: Disable recording, logs, or CAPTCHA solving when they are unnecessary, and review Browserbase dashboard artifacts before sharing or retaining them. <br>
Risk: The release includes an under-disclosed ChatGPT/Suno automation script. <br>
Mitigation: Review or remove scripts/dedication_automation.mjs before installation if that automation is outside the intended use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JamesFincher/browserbase-sessions) <br>
- [Browserbase documentation](https://docs.browserbase.com) <br>
- [Browserbase API quick reference](references/api-quick-ref.md) <br>
- [Browserbase API base URL](https://api.browserbase.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON configuration examples, and command outputs from Browserbase automation scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create persistent browser contexts, live debugger links, screenshots, rrweb recording event files, log output, cookies, downloads archives, and local workspace state.] <br>

## Skill Version(s): <br>
2.5.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
