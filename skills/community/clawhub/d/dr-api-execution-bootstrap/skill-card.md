## Description: <br>
Bootstrap and enforce fast direct API execution in a workspace for repeated CRUD, integration, service-compliance, and other multi-call API operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniel-refahi-ikara](https://clawhub.ai/user/daniel-refahi-ikara) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to persist direct API execution defaults, run one upfront preflight, execute approved API chains continuously, and validate workspace behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently changes workspace agent behavior toward direct API execution. <br>
Mitigation: Review the exact AGENTS.md, MEMORY.md, or equivalent startup-file diff before accepting the change. <br>
Risk: The skill can run live API validation and side-effecting API workflows when credentials are available. <br>
Mitigation: Confirm the environment is dev or test, require approval for write operations, and approve any live validation before execution. <br>
Risk: The security review marked the release suspicious and advises review before installation. <br>
Mitigation: Install only when this direct-execution behavior is intentional and the required credentials, endpoints, and approval boundaries are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniel-refahi-ikara/dr-api-execution-bootstrap) <br>
- [Apply checklist](references/APPLY.md) <br>
- [Execution playbook](references/EXECUTION-PLAYBOOK.md) <br>
- [Ikara API patterns](references/IKARA-PATTERNS.md) <br>
- [Installation and activation](references/INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify workspace startup files and report validation status.] <br>

## Skill Version(s): <br>
1.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
