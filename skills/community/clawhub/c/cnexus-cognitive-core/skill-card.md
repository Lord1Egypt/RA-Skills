## Description:

CNexus 2.0 is a local personal second-brain skill for cognitive conversation, memory graphs, JSON persistence, one-click memory clearing, and a Python standard-library plus static UI runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plusunm](https://clawhub.ai/user/plusunm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install and run CNexus 2.0 as a local personal knowledge and cognitive-memory application. It supports conversation, memory graph status, memory clearing, REM-style organization, code ingestion, and image ingestion workflows described by the artifact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact does not include the CNexus runtime code, so installation depends on mutable external code from GitHub or OpenClaw.

Mitigation: Use a pinned commit or signed release, review the runtime before executing it, and install only from a source you trust.

Risk: The skill supports clearing persisted local memory through the UI and the POST /api/memory/clear endpoint.

Mitigation: Back up the CNexus memory file before using clear-memory functionality.

## Reference(s):

- [CNexus2.0 GitHub repository](https://github.com/plusunm/CNexus2.0)
- [Server-resolved GitHub import path](https://github.com/plusunm/CNexus2.0/tree/main/clawhub/cnexus-cognitive-core)
- [ClawHub skill page](https://clawhub.ai/plusunm/skills/cnexus-cognitive-core)
- [plusunm publisher profile](https://clawhub.ai/user/plusunm)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash commands, endpoint references, and concise setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs users to clone and run an external GitHub repository; the reviewed artifact does not include the runtime code.]

## Skill Version(s):

1.10.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
