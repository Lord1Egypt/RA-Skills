## Description: <br>
Monitors AI agents in real time to detect anomalies, enforce safety policies, and trigger emergency shutdowns that help prevent damage and cost overruns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhenStaff](https://clawhub.ai/user/ZhenStaff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Emergency Circuit to monitor AI agent activity, enforce resource and safety policies, and trigger manual or automatic shutdown when an agent violates limits or behaves anomalously. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Emergency shutdown and auto-kill policies can stop active workflows or leave external actions partially complete. <br>
Mitigation: Test policies in sandbox mode, use explicit agent IDs, and confirm operational impact before enabling production kill controls. <br>
Risk: Monitoring logs and incident data may contain sensitive operational information. <br>
Mitigation: Confirm how logs and incident data are stored, retained, and accessed before deployment. <br>
Risk: External npm or GitHub implementations need verification before installation. <br>
Mitigation: Review the external package or repository source and confirm it matches the intended release before installing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ZhenStaff/emergency-circuit) <br>
- [npm package](https://www.npmjs.com/package/openclaw-emergency-circuit) <br>
- [GitHub project](https://github.com/ZhenRobotics/openclaw-emergency-circuit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI examples, policy JSON, and TypeScript integration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include monitoring commands, emergency-stop commands, policy templates, troubleshooting steps, and installation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
