## Description: <br>
Manage multiple SaaS startups simultaneously with CEO-driven orchestration, product agents, ChatDev code generation, and a 3-Gate BUILD, TEST, JUDGE pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[csbenson001](https://clawhub.ai/user/csbenson001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and startup operators use this skill to coordinate multiple SaaS product repositories through CEO-led prioritization, product-agent execution, ChatDev-assisted code generation, and build, test, and judge review gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run a setup step that is not present in the artifact for review. <br>
Mitigation: Obtain and inspect the missing setup script before installation, and run setup only in a sandboxed repository or branch. <br>
Risk: The skill enables broad multi-agent code automation across product repositories without enough stated boundaries. <br>
Mitigation: Avoid production data, customer data, deployment credentials, and unattended schedules until approval gates, redaction, logging, retention, and stop controls are defined. <br>
Risk: The skill depends on ChatDev-based code generation. <br>
Mitigation: Pin and review the ChatDev dependency before use, and require human review before generated code is merged or deployed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/csbenson001/dark-factory-skill) <br>
- [ChatDev](https://github.com/OpenBMB/ChatDev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose repository changes, setup commands, product-agent routing, quality-gate assessments, and improvement-loop actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
