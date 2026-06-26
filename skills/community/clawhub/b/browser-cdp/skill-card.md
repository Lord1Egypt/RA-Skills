## Description: <br>
Real Chrome browser automation via CDP Proxy for using logged-in browser state, interacting with pages, extracting dynamic content, and taking screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xcjl](https://clawhub.ai/user/0xcjl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when static fetching is blocked, logged-in browser state is needed, or a task requires browser interaction such as clicking, filling forms, scrolling, navigation, screenshots, or JavaScript-rendered content extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can provide broad control over a logged-in local Chrome session through an unauthenticated localhost proxy. <br>
Mitigation: Run it only when browser control is intended, use a dedicated temporary Chrome profile, avoid sensitive accounts and sites, and stop the proxy immediately after the task. <br>
Risk: JavaScript evaluation, clicks, screenshots, navigation, and file uploads can expose or alter private browser state. <br>
Mitigation: Review agent actions before execution, restrict use to task-relevant tabs and accounts, and treat screenshots, file upload paths, and page-derived data as sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xcjl/browser-cdp) <br>
- [Usage log](references/usage-log.md) <br>
- [Original web-access project](https://github.com/eze-is/web-access) <br>
- [Original project issue fixed in this skill](https://github.com/eze-is/web-access/issues/10) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, code, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser screenshots or page-derived text when the proxy is used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
