## Description: <br>
Manages agent progress reporting and OKF-compliant memory syncing to Fulcra. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fulcra](https://clawhub.ai/user/fulcra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to maintain Fulcra-backed progress reports, role files, session summaries, task records, knowledge files, and inbox archives in an OKF-compliant memory namespace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External memory uploads could include sensitive user data, credentials, or private internal reasoning if generated memory files are not reviewed. <br>
Mitigation: Review progress, session, task, role, and knowledge files before upload, minimize disclosures, and follow the skill's privacy requirement. <br>
Risk: Inbox cleanup can delete source items after processing if archive upload is incomplete or misnamed. <br>
Mitigation: Confirm the archive upload and timestamped archive path before deleting inbox files. <br>


## Reference(s): <br>
- [Fulcra Memory CLI Reference](references/fulcra-memory-cli.md) <br>
- [Fulcra onboarding CLI documentation](https://raw.githubusercontent.com/fulcradynamics/agent-skills/main/skills/fulcra-onboarding/references/fulcra-cli.md) <br>
- [Open Knowledge Format specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) <br>
- [Fulcra Memory on ClawHub](https://clawhub.ai/fulcra/skills/fulcra-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file path conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OKF-oriented memory file guidance and Fulcra CLI commands for progress, role, session, task, knowledge, and inbox workflows.] <br>

## Skill Version(s): <br>
0.0.8 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
