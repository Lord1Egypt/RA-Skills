## Description: <br>
1Panel server management panel one-click installation skill that detects existing installations, returns access information when present, and runs the installation flow when absent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jack-Liang](https://clawhub.ai/user/Jack-Liang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and server operators use this skill to install or inspect a 1Panel server management panel from an agent conversation. It automates dependency checks, root permission checks, installation, service startup validation, and reporting of generated panel access details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installation flow can make root-level server changes. <br>
Mitigation: Run it only on a server you control, review the remote package source first, and require explicit confirmation before executing install.sh. <br>
Risk: Returned panel credentials can be exposed through chat logs or screenshots. <br>
Mitigation: Protect generated username and password values, change the panel password immediately after installation, and restrict panel network access. <br>
Risk: The bundled test script can disrupt an existing 1Panel installation. <br>
Mitigation: Do not run test.sh on a production host. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jack-Liang/1panel-install) <br>
- [1Panel v2.1.4 release package](https://resource.fit2cloud.com/1panel/package/v2/stable/v2.1.4/release/1panel-v2.1.4-linux-amd64.tar.gz) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style natural language with command output and access details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated panel address, username, password, troubleshooting guidance, and security reminders.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
