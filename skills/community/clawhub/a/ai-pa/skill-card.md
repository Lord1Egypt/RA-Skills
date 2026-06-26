## Description: <br>
AI Personal Assistant network skill for multi-agent PA coordination, including PA contact lookup, peer-agent coordination, meeting scheduling, PA group broadcasts, and local PA directory use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and delegated personal assistant agents use this skill to coordinate with peer PAs, look up PA contacts from a local directory, schedule meetings between owners, broadcast coordination messages, and send owner-approved email or calendar actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive PA and owner contact data. <br>
Mitigation: Install only in trusted workspaces and remove or replace real-looking example contact entries before use. <br>
Risk: The skill can guide agents through delegated owner email, calendar, authentication, and directory update actions. <br>
Mitigation: Require explicit owner approval before email sends, calendar creation, account authentication steps, or directory updates. <br>
Risk: Loading local context from a .context file can execute shell content if the workspace is not controlled. <br>
Mitigation: Avoid sourcing .context as shell unless the file is controlled and reviewed by the workspace owner. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples and inline shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance and command templates for local PA directory lookup, validation, updates, messaging, email, and calendar workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
