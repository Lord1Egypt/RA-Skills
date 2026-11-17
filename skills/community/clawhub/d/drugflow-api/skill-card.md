## Description:

Multi-flow API workflow skill for this DrugFlow Django repository. Use when an agent needs executable end-to-end API procedures such as login/register, workspace and balance retrieval, job listing, virtual screening, docking, ADMET, rescoring, structure extraction, and molecular factory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashipiling](https://clawhub.ai/user/ashipiling)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to select and execute DrugFlow API workflows for authentication, workspace and balance checks, job listing, virtual screening, docking, ADMET, rescoring, structure extraction, and molecular factory tasks. It returns the API steps, required parameters, key identifiers, job state, result counts, and important script outputs needed to operate those flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles credentials for DrugFlow sessions.

Mitigation: Install only for trusted DrugFlow endpoints, prefer HTTPS, avoid passing real passwords on the command line, and protect and delete cookie jars.

Risk: The skill can upload data and create remote jobs that may consume tokens.

Mitigation: Use test accounts and non-sensitive datasets first, and require explicit user approval before signup, workspace creation, uploads, or job submission.

## Reference(s):

- [DrugFlow Skill Page](https://clawhub.ai/ashipiling/skills/drugflow-api)
- [DrugFlow Flow Index](references/index.md)
- [Common APIs Call Flow](references/flows/common-apis/call-flow.md)
- [Common APIs Payload Rules](references/flows/common-apis/payloads.md)
- [Virtual Screening Call Flow](references/flows/virtual-screening/call-flow.md)
- [Virtual Screening Payload Notes](references/flows/virtual-screening/payloads.md)
- [Docking Call Flow](references/flows/docking/call-flow.md)
- [Docking Payload Notes](references/flows/docking/payloads.md)
- [ADMET Call Flow](references/flows/admet/call-flow.md)
- [ADMET Payload Notes](references/flows/admet/payloads.md)
- [Molecular Factory Call Flow](references/flows/molecular-factory/call-flow.md)
- [Molecular Factory Payload Notes](references/flows/molecular-factory/payloads.md)
- [Rescoring Call Flow](references/flows/rescoring/call-flow.md)
- [Rescoring Payload Notes](references/flows/rescoring/payloads.md)
- [Structure Extract Call Flow](references/flows/structure-extract/call-flow.md)
- [Structure Extract Payload Notes](references/flows/structure-extract/payloads.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with API endpoint summaries, JSON payloads, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes method, endpoint, required parameters, key identifiers such as ws_id and job_id, job state, result count, and important script output.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
