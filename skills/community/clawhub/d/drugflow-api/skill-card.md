## Description: <br>
Multi-flow API workflow skill for this DrugFlow Django repository that helps an agent run end-to-end API procedures for login/register, workspace and balance retrieval, job listing, virtual screening, docking, ADMET, rescoring, structure extraction, and molecular factory workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashipiling](https://clawhub.ai/user/ashipiling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to select and execute DrugFlow API workflows, including account/session setup, workspace management, token balance checks, job creation, polling, and result retrieval for computational drug discovery tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent operate a real DrugFlow account, upload molecular data, and create token-consuming jobs. <br>
Mitigation: Use a low-privilege account, confirm before uploads or job creation, and review expected token use before execution. <br>
Risk: Session cookies and account credentials may be exposed if included directly in commands or left in persistent cookie files. <br>
Mitigation: Avoid putting passwords directly in command history, protect cookie files, and delete session artifacts after use. <br>
Risk: An incorrect or untrusted DrugFlow base URL could send credentials or proprietary molecular data to the wrong service. <br>
Mitigation: Verify the target DrugFlow URL before signing in, uploading files, or creating jobs. <br>


## Reference(s): <br>
- [DrugFlow skill page](https://clawhub.ai/ashipiling/drugflow-api) <br>
- [DrugFlow Flow Index](references/index.md) <br>
- [Common APIs Call Flow](references/flows/common-apis/call-flow.md) <br>
- [Common APIs Payload Rules](references/flows/common-apis/payloads.md) <br>
- [Virtual Screening Call Flow](references/flows/virtual-screening/call-flow.md) <br>
- [Virtual Screening Payload Notes](references/flows/virtual-screening/payloads.md) <br>
- [Docking Call Flow](references/flows/docking/call-flow.md) <br>
- [Docking Payload Notes](references/flows/docking/payloads.md) <br>
- [ADMET Call Flow](references/flows/admet/call-flow.md) <br>
- [ADMET Payload Notes](references/flows/admet/payloads.md) <br>
- [Rescoring Call Flow](references/flows/rescoring/call-flow.md) <br>
- [Rescoring Payload Notes](references/flows/rescoring/payloads.md) <br>
- [Structure Extract Call Flow](references/flows/structure-extract/call-flow.md) <br>
- [Structure Extract Payload Notes](references/flows/structure-extract/payloads.md) <br>
- [Molecular Factory Call Flow](references/flows/molecular-factory/call-flow.md) <br>
- [Molecular Factory Payload Notes](references/flows/molecular-factory/payloads.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with API steps, endpoint details, JSON payloads, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns method and endpoint details, required parameters, key ids and state such as ws_id, job_id, state, result count, and important script outputs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
