## Description: <br>
Control the host machine's Chrome browser to open specific URLs in new tabs when the user explicitly asks to open a link, show a page, or search in the browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenxie66](https://clawhub.ai/user/stevenxie66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they want an agent to open a specific HTTP or HTTPS URL in the user's real Chrome browser rather than perform internal or headless browsing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens user-requested URLs in the user's real Chrome browser, which may expose logged-in sessions or sensitive browser state to the opened page. <br>
Mitigation: Confirm the exact URL before use, avoid sensitive logged-in sessions, and prefer a dedicated browser profile for stronger separation. <br>
Risk: The skill requires Chrome remote debugging to be enabled on the host machine. <br>
Mitigation: Use it only in environments where the remote debugging port is intentionally enabled and access to that port is controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stevenxie66/control-host-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance] <br>
**Output Format:** [Text status messages and shell command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Opens a new Chrome tab through Chrome DevTools Protocol and reports success or error details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
