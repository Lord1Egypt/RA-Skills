## Description: <br>
Create a new Bob agent only on explicit operator command using a guarded replication runner. Purposeful Bobiverse-style replication for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theamericanmaker](https://clawhub.ai/user/theamericanmaker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw operators use this skill to create a purpose-scoped peer Bob agent only after an explicit replication request, a concrete mission need, a dry-run preview, and nonce-backed approval. It supports personality variation, memory-policy selection, lineage tracking, and local agent registration for Unix-like OpenClaw workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent new OpenClaw clone workspaces. <br>
Mitigation: Install only for intentional agent-management use, review the dry-run plan, and require the exact nonce-backed confirmation token before execution. <br>
Risk: A clone may inherit workspace files and memory from the parent depending on the selected memory policy. <br>
Mitigation: Choose the memory policy deliberately and inspect the dry-run output before approving execution. <br>
Risk: Workspace duplication and agent registration affect local OpenClaw state. <br>
Mitigation: Use only the guarded runner, which validates workspace boundaries, rejects symlinks, stages changes transactionally, audits attempts, and rolls back failed execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/theamericanmaker/bobiverse-replicate) <br>
- [README](README.md) <br>
- [Architecture](ARCHITECTURE.md) <br>
- [Security Model](SECURITY.md) <br>
- [Serial Number Specification](SERIAL-NUMBER-SPEC.md) <br>
- [Bobiverse Primer](docs/bobiverse-primer.md) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Project homepage](https://github.com/TheAmericanMaker/bobiverse-openclaw) <br>
- [Support](https://github.com/TheAmericanMaker/bobiverse-openclaw/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with guarded shell-command execution and local workspace file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw and python3 on darwin or linux; execution is dry-run first and requires an exact nonce-backed confirmation token.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
