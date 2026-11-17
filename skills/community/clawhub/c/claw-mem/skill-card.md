## Description:

Lightweight memory management system for OpenClaw with 3-tier retrieval (L0/L1/L2), automatic lifecycle monitoring, and advanced search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leohuang8688](https://clawhub.ai/user/leohuang8688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use ClawMem to add local, tiered memory storage, retrieval, lifecycle monitoring, and search to OpenClaw agents while limiting routine token use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local long-term memory can retain sensitive agent session data, tool-call payloads, and memory-write content.

Mitigation: Enable lifecycle monitoring only with explicit opt-in, treat the SQLite database as sensitive, and require redaction plus retention or deletion controls before deployment.

Risk: Automatic lifecycle monitoring may capture more operational context than users expect.

Mitigation: Keep monitored event types narrow and documented, avoid sending secrets through monitored events, and protect stored records with encryption or strict file permissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leohuang8688/skills/claw-mem)
- [ClawMem README](README.md)
- [ClawMem Search Guide](docs/SEARCH_GUIDE.md)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Claude-Mem Documentation](https://docs.claude-mem.ai/)
- [Project repository link from README](https://github.com/leohuang8688/clawmem)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript examples, bash commands, configuration values, and runtime JavaScript object results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores and retrieves local L0/L1/L2 memory records; full details are loaded only when requested.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact package.json reports 0.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
