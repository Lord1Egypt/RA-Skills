## Description:

Uses the Datris MCP server as a long-term semantic memory layer by syncing local markdown memory files into a Datris vector retrieval index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datris](https://clawhub.ai/user/datris)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to bootstrap, sync, and query long-term memory while keeping local markdown files canonical. It supports memory-shaped requests such as saving, recalling, ingesting, syncing, and searching notes through Datris.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local long-term memory files may be uploaded to Datris for persistent indexing and recurring synchronization.

Mitigation: Confirm the Datris endpoint and tenant before use, decide which memory files may be uploaded, and exclude sensitive notes, credentials, and secrets.

Risk: Broad or repeated sync can run without clear per-file consent controls.

Mitigation: Require an explicit sync scope before bootstrap or recurring sync, and keep an audit of files uploaded, deleted, and verified.

Risk: Indexed memory may remain available after sync unless deletion and disablement paths are confirmed.

Mitigation: Verify there is a way to disable sync and delete indexed Datris data before using the skill with private memory.

## Reference(s):

- [Datris Memory ClawHub release](https://clawhub.ai/datris/skills/datris-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Datris MCP workflow steps and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Datris MCP operations for uploads, deletes, job polling, vector search, and sync audit entries.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
