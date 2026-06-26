## Description: <br>
Optimizes memory management by scoring, pruning low-value entries, controlling size, and smartly retrieving top relevant memories for efficient access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daxiangnaoyang](https://clawhub.ai/user/daxiangnaoyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage long-running agent memory stores by scoring relevance, retrieving the most useful memories, and pruning or archiving low-value entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic pruning or archiving can remove or move stored memories before a user verifies that they are low value. <br>
Mitigation: Back up memory files, run pruning in dry-run or approval mode first, verify the archive destination, and test relevance thresholds on non-critical memory stores. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daxiangnaoyang/daxiang-memory-optimization) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Artifact configuration](artifact/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, PowerShell, JSON, and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides configurable thresholds for pruning, memory window size, retrieval count, archive location, cache TTL, and batch size.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
