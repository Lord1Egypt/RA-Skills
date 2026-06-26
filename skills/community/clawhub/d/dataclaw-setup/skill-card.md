## Description: <br>
Setup guide for installing and configuring DataClaw for OpenClaw; it explains DataClaw and initial setup, while the per-access-point OpenClaw database connection skill is installed later from the DataClaw UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ddanieli](https://clawhub.ai/user/ddanieli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to understand DataClaw and complete the initial setup steps before installing a generated access-point skill from the DataClaw UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A generated DataClaw access-point skill may later grant database access, including raw SQL, writes, or execute permissions. <br>
Mitigation: Install DataClaw only from trusted sources, use least-privilege database credentials, prefer approved queries, and separately review generated DataClaw skills before enabling broad permissions. <br>
Risk: Users may mistake this setup guide for an active DataClaw database connection. <br>
Mitigation: Confirm DataClaw is installed, running, configured with a datasource, and that the DataClaw UI has installed the specific access-point skill before attempting database operations. <br>


## Reference(s): <br>
- [DataClaw Website](https://dataclaw.sh) <br>
- [DataClaw GitHub Repository](https://github.com/ekaya-inc/dataclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown setup guidance with ordered steps, bullet lists, and inline command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not run commands, install DataClaw, connect to databases, or create a per-access-point skill by itself.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
