## Description: <br>
Helps agents remotely debug Android Chrome or Edge browser tabs over USB using ADB port forwarding and the Chrome DevTools Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sougannkyou](https://clawhub.ai/user/sougannkyou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect an agent to Android browser debugging sessions, inspect console and network behavior, capture DOM or screenshots, and run reviewed JavaScript diagnostics through CDP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ADB forwarding and CDP access can expose browser tabs on connected Android devices. <br>
Mitigation: Use the skill only with devices and tabs you control, close unrelated sensitive pages, and remove ADB forwards after debugging. <br>
Risk: Runtime.evaluate examples can execute JavaScript in the target page and may read or change page data. <br>
Mitigation: Review JavaScript expressions before running them and avoid using the skill on sensitive pages. <br>
Risk: Temporary scripts, screenshots, and captured output may contain private page data. <br>
Mitigation: Delete temporary scripts and captured output after the debugging session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sougannkyou/android-remote-browser-debug) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ADB and CDP setup steps, diagnostic expressions, troubleshooting notes, and cleanup commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
