## Description: <br>
Enable agents to collaborate using shared memory, team inboxes, and user artifacts via Fulcra's versioned file storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fulcra](https://clawhub.ai/user/fulcra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to coordinate agent teams through Fulcra shared storage, including artifact uploads, team inbox messaging, and shared progress and task records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared team storage can persist or expose user context, generated files, or workspace content to other agents. <br>
Mitigation: Share content only after explicit authorization and only with agents that are authorized to receive it. <br>
Risk: Optional heartbeats or cron jobs can repeatedly read, write, archive, or delete team files beyond the user's intent. <br>
Mitigation: Before enabling automation, define the team name, agent name, frequency, duration, and allowed file actions. <br>
Risk: Uploaded artifacts or team messages may contain secrets or private workspace data. <br>
Mitigation: Review content before upload and avoid storing secrets or private material unless every receiving agent is authorized. <br>


## Reference(s): <br>
- [Fulcra Agent Teams on ClawHub](https://clawhub.ai/fulcra/skills/fulcra-agent-teams) <br>
- [Fulcra Agent Teams CLI Reference](references/fulcra-agent-teams-cli.md) <br>
- [Fulcra CLI Documentation](https://raw.githubusercontent.com/fulcradynamics/agent-skills/main/skills/fulcra-onboarding/references/fulcra-cli.md) <br>
- [Open Knowledge Format Specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Fulcra file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Fulcra-backed team, member, inbox, archive, task, session, knowledge, and artifact files when authorized.] <br>

## Skill Version(s): <br>
0.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
