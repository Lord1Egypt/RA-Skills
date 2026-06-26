## Description: <br>
Lightweight memory management system for OpenClaw with 3-tier retrieval (L0/L1/L2), automatic lifecycle monitoring, and advanced search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leohuang8688](https://clawhub.ai/user/leohuang8688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use ClawMem to add local persistent memory, tiered retrieval, lifecycle event capture, and search to OpenClaw agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically record and retain detailed local agent activity. <br>
Mitigation: Enable it only when persistent local memory is intended, decide which event types may be captured, and configure retention or deletion controls before use. <br>
Risk: Captured memory may contain secrets, regulated data, or sensitive user activity. <br>
Mitigation: Avoid storing sensitive data, add redaction before writing memory records, and restrict who or what can query detailed historical memory. <br>


## Reference(s): <br>
- [ClawMem release page](https://clawhub.ai/leohuang8688/claw-mem) <br>
- [Search Guide](docs/SEARCH_GUIDE.md) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [Claude-Mem documentation](https://docs.claude-mem.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JavaScript and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local SQLite-backed memory operations and retrieval guidance for OpenClaw agents.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact package.json reports 0.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
