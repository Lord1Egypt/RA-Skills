## Description: <br>
Build and run low-code browser automation workflows with agent-browser CLI and reusable skills for repeatable browser tasks such as sign-ins, form filling, fixed click flows, state saving, and recurring web operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnxufei-tech](https://clawhub.ai/user/cnxufei-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to convert stable, repetitive browser workflows into reusable agent-browser command sequences or site-specific skills. It is most useful when tasks can be discovered once, rerun many times, and verified through fresh snapshots or saved browser state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved browser state files can grant access to authenticated sessions. <br>
Mitigation: Treat auth.json or similar saved state as a password: keep it out of source control, store it in a protected location, use separate files per site or account, and delete or rotate it when no longer needed. <br>
Risk: Browser automation may interact with sites or accounts where the user lacks permission. <br>
Mitigation: Use the skill only for sites and workflows the user is authorized to automate, and verify target-site rules before running recurring flows. <br>


## Reference(s): <br>
- [Source Notes](references/source-notes.md) <br>
- [ClawHub Release Page](https://clawhub.ai/cnxufei-tech/browser-automation-zero-token) <br>
- [Publisher Profile](https://clawhub.ai/user/cnxufei-tech) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell command examples and reusable workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include saved-state guidance for recurring authenticated browser sessions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
