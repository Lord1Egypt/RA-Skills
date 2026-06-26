## Description: <br>
Persistent cloud memory across sessions that automatically recalls past decisions, code, and tasks before each request, saves summaries after each session, and provides manual Bash tools for searching, recording, and querying memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[everest-an](https://clawhub.ai/user/everest-an) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to maintain persistent cloud-backed memory across sessions, retrieve prior decisions and tasks, and record new implementation context through automatic hooks or manual Node.js commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic hooks may send prompts, search queries, memory records, task/session metadata, and recalled context to a remote cloud memory service. <br>
Mitigation: Install only when cloud memory is intended; prefer local mode or a narrowly scoped memory for sensitive work, and avoid entering secrets or regulated/customer data. <br>
Risk: Setup can persist credentials in shell profiles, and logout may not clean up every exported credential. <br>
Mitigation: Review and remove shell profile exports when disabling the skill, and rotate credentials if they may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/everest-an/awareness-cloud-memory) <br>
- [Awareness service](https://awareness.market) <br>
- [Awareness API endpoint](https://awareness.market/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [XML memory context blocks, JSON responses, and Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Automatic hooks can inject recalled context before prompts and save session checkpoints after responses when configured.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
