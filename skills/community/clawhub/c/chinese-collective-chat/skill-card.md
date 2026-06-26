## Description: <br>
Manages inter-agent collective chat communication for an Axioma Stellaris cluster, including queue checks, ordered message writes, and chat history review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or developers operating the specified Merlin/Axioma shared local environment use this skill to coordinate agent turns, inspect shared queue state, write collective chat messages, and log waiting state to agent journals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad authority to change shared state, write to other agents' journals, and trigger recovery or escalation actions without clear safeguards. <br>
Mitigation: Add explicit approval and authorization rules before auto-heal, wake attempts, human notification, backup recovery, lock deletion, or any write to another agent's journal. <br>
Risk: The skill is intended for a specific Merlin/Axioma shared local environment and includes fixed shared-folder paths. <br>
Mitigation: Install only in the intended environment, verify the shared paths and participating agents, and avoid running it against unrelated local or mounted directories. <br>
Risk: Queue repair, lock handling, and retry behavior can corrupt coordination state if invoked on stale or unauthorized data. <br>
Mitigation: Require state backups and manual review before restoring queues, deleting lock files, or retrying failed writes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/chinese-collective-chat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct writes to shared chat, queue, lock, and agent journal files in the configured local environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact version table) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
