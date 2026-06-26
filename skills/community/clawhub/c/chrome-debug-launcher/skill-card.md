## Description: <br>
Launch two independent Chrome browser instances, one normal and one with remote debugging enabled on port 9222. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengzongxin](https://clawhub.ai/user/chengzongxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to open a normal Chrome session alongside a Chrome instance that Selenium or Playwright can attach to through localhost port 9222. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can close existing Chrome windows before launching new browser instances. <br>
Mitigation: Confirm there is no unsaved browser work before use and prefer an implementation that isolates the debug profile without terminating active sessions. <br>
Risk: The skill opens a Chrome instance with remote debugging enabled on port 9222. <br>
Mitigation: Keep the debug browser open only while needed and restrict use to trusted local automation workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chengzongxin/chrome-debug-launcher) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with PowerShell and bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands launch Chrome with remote debugging on port 9222 and a separate user data directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
