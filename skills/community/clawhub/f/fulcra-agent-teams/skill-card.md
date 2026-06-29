## Description: <br>
Enable agents to collaborate using shared memory, team inboxes, and user artifacts via Fulcra's versioned file storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fulcra](https://clawhub.ai/user/fulcra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate work across agents through Fulcra shared storage, including approved artifact uploads, team inbox messages, archive handling, and OKF-style team progress files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cross-agent coordination can expose private workspace data to recipients who are not authorized to receive it. <br>
Mitigation: Confirm the allowed Fulcra team paths and recipients before use, and require explicit authorization before transferring context or files between agents. <br>
Risk: Uploaded artifacts or inbox messages may contain sensitive user data. <br>
Mitigation: Approve each artifact upload and avoid placing sensitive data in shared team inboxes unless every recipient is authorized. <br>
Risk: Automated inbox checks create persistent periodic processing. <br>
Mitigation: Enable background inbox checks only after user consent and keep processing scoped to the approved team inbox path. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fulcra/fulcra-agent-teams) <br>
- [Fulcra Agent Teams CLI Reference](references/fulcra-agent-teams-cli.md) <br>
- [Fulcra CLI documentation](https://raw.githubusercontent.com/fulcradynamics/agent-skills/main/skills/fulcra-onboarding/references/fulcra-cli.md) <br>
- [Open Knowledge Format specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and Fulcra path conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user approval for artifact uploads and cross-agent data transfer; automated inbox checks require user consent.] <br>

## Skill Version(s): <br>
0.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
