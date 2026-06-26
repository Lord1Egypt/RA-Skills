## Description: <br>
Always-on self-awareness framework for OpenClaw agents that helps them verify platform mechanics, memory layers, storage conventions, context health, and common failure modes before answering or acting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inxan3](https://clawhub.ai/user/inxan3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep OpenClaw agents grounded in platform behavior, memory and storage practices, failure handling, and /selfcheck routines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends persistent weekly self-check automation and drift logs, which can create ongoing actions or stored state if accepted without review. <br>
Mitigation: Approve the exact schedule, paths, stored contents, and removal method before allowing setup; omit persistence when it is not needed. <br>
Risk: The security review warns that credential-related storage guidance could lead users to put secrets in workspace memory files. <br>
Mitigation: Use platform secret stores or environment-managed secrets for credentials, and avoid writing API keys or tokens to memory files. <br>


## Reference(s): <br>
- [OpenClaw Docs](https://docs.openclaw.ai) <br>
- [Platform Truths](references/platform-truths.md) <br>
- [Storage Conventions](references/storage-conventions.md) <br>
- [Failure Protocol](references/failure-protocol.md) <br>
- [Drift Catalog](references/drift-catalog.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent cron setup and memory/drift-log file creation; user approval should gate those actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
