## Description: <br>
Desktop Monitor Widget opens a local desktop or browser-based system monitor that shows CPU, memory, disk, temperature, uptime, and process count. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1173910773](https://clawhub.ai/user/1173910773) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to launch a lightweight local monitor for real-time system resource status. It is intended for personal desktop visibility into CPU, memory, disk, temperature, uptime, and process count. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The startup script can automatically change the Python environment by installing psutil, including with --break-system-packages. <br>
Mitigation: Review before installing, prefer a virtual environment, and remove the --break-system-packages install path before deployment. <br>
Risk: The browser mode exposes live local system metrics through a localhost endpoint with a permissive CORS header. <br>
Mitigation: Restrict or remove the permissive CORS header and only run the endpoint in trusted local contexts. <br>
Risk: While running, the widget makes CPU, memory, disk, uptime, temperature, and process count available from the local endpoint. <br>
Mitigation: Stop the widget when not needed and avoid running it on shared or sensitive machines without review. <br>


## Reference(s): <br>
- [README.md](artifact/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/1173910773/desktop-monitor-widget) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local UI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The launched widget refreshes local system metrics every 2 seconds.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
