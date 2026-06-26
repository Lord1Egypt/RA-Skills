## Description: <br>
Automated guided vehicle route planner. Use when json agv tasks, csv agv tasks, checking agv status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can invoke this CLI-style skill to add, list, search, remove, export, and configure local AGV-labeled entries. Based on the security review, treat it as a local note/config tracker rather than an authoritative AGV routing or vehicle-status system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is labeled as an AGV route planner, but security evidence says it behaves like a local note/config store that can persist, delete, and export arbitrary entries. <br>
Mitigation: Use it only for simple local entry tracking; do not rely on it for real AGV routing, vehicle status, facility operations, or industrial automation. <br>
Risk: Local entries and configuration may be persisted under the user's home directory and exported into the current working directory. <br>
Mitigation: Review stored data before export or deletion, set AGV_DIR deliberately when isolation is needed, and avoid entering sensitive operational data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/agv) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Plain text CLI output, JSONL local data, and JSON or CSV exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entries under ~/.agv by default, or under AGV_DIR when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
