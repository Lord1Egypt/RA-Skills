## Description: <br>
Delx Wellness helps agents choose, install, and combine local-first wellness MCP connectors using a public registry and setup guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidmosiah](https://clawhub.ai/user/davidmosiah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents, developers, and operators use this skill to select wearable, activity, and nutrition MCP connectors, compare provider coverage, and apply Delx Wellness setup and safety guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analytics-related commands may use credentials or reach live providers. <br>
Mitigation: Confirm required credentials before running commands, use read-only or least-privilege access, and obtain explicit approval before live provider calls or writes. <br>
Risk: Provider setup can involve OAuth tokens, API keys, service-account JSON, token files, or private user data. <br>
Mitigation: Keep provider credentials in local connector setup, never print secrets or private user data, and prefer dry-run, doctor, manifest, privacy_audit, or connection_status checks before write operations. <br>
Risk: Wellness connector recommendations could be mistaken for medical, legal, financial, or platform-policy advice. <br>
Mitigation: Present recommendations as connector selection and setup guidance only, and keep user consent explicit for provider access or data handling. <br>


## Reference(s): <br>
- [Delx Wellness Connector Registry](https://wellness.delx.ai) <br>
- [Delx Wellness Connectors Catalog](https://wellness.delx.ai/connectors) <br>
- [Delx Wellness Repository](https://github.com/davidmosiah/delx-wellness) <br>
- [ClawHub Delx Wellness Release](https://clawhub.ai/davidmosiah/delx-wellness) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with connector recommendations, setup notes, safety boundaries, troubleshooting steps, and inline shell commands when relevant.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference public registry metadata and requires explicit handling of provider credentials outside this registry skill.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
