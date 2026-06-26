## Description: <br>
Cognitive Topology helps an agent split complex tasks into independent branches, run them in parallel, and synthesize branch conclusions from L2 files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiushang555](https://clawhub.ai/user/qiushang555) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multi-angle analysis or independent subtasks through branch creation, status tracking, integration, and optional memory archiving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write task text and branch conclusions into long-term local memory without a clear opt-in. <br>
Mitigation: Use it only on content approved for local retention, or disable or gate the archive workflow before handling secrets, personal data, private business material, or regulated content. <br>
Risk: The skill coordinates subagents and local workspace files, including fixed OpenClaw workspace paths. <br>
Mitigation: Review generated branch tasks and confirm the OpenClaw workspace paths are intended before running the helper scripts. <br>


## Reference(s): <br>
- [Cognitive Topology reference guide](references/topology-guide.md) <br>
- [ClawHub release page](https://clawhub.ai/qiushang555/cognitive-topology) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local topology, branch L2, synthesis, and memory files under the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
