## Description: <br>
Provides isolated NVIDIA OpenShell sandboxes for code execution, security scans, debugging, and test runs with resource and network restrictions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sabatech-dev](https://clawhub.ai/user/sabatech-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and specialist coding, security, debugging, and QA agents use this skill to run commands, tests, scans, and troubleshooting steps inside named OpenShell sandboxes instead of directly on the host. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to execute arbitrary commands, security scans, and tests inside OpenShell sandboxes. <br>
Mitigation: Install only in trusted OpenShell environments, verify the CLI and gateway, and explicitly approve security scans or other sensitive command execution. <br>
Risk: Network policy changes or file transfers between host and sandbox can expand access beyond the intended isolated workflow. <br>
Mitigation: Keep network access restricted by default, review policy changes before applying them, and approve sandbox file transfers deliberately. <br>
Risk: Sandbox behavior depends on the configured image, sandbox policies, and local OpenShell setup. <br>
Mitigation: Verify the image source, sandbox policies, and resource limits before relying on the sandbox for isolation. <br>


## Reference(s): <br>
- [Alfred OpenShell Sandbox ClawHub page](https://clawhub.ai/sabatech-dev/alfred-openshell-sandbox) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No bundled executable code; the skill guides an agent to invoke an existing OpenShell CLI and sandbox setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
