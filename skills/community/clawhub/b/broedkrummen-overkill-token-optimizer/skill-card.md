## Description:

Optimize and manage session tokens for workspace memory with commands to check usage, reset, index, search, and compress tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[broedkrummen](https://clawhub.ai/user/broedkrummen)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to inspect token usage, index and search OpenClaw session memory, and run command output through oktk compression when they need to reduce context size.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions and dependency handling can ask users to run mutable third-party code with broad local privileges.

Mitigation: Install only a pinned, verified oktk release or use a trusted local oktk binary before enabling compression commands.

Risk: The skill may read OpenClaw session memory and create a local index.

Mitigation: Avoid use on sensitive sessions unless local indexing and session-memory access are acceptable for the workspace.

Risk: Compression commands run user commands through oktk.

Mitigation: Review commands before execution and prefer dry-run or inspection workflows for unfamiliar commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/broedkrummen/skills/broedkrummen-overkill-token-optimizer)
- [oktk dependency](https://github.com/satnamra/oktk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local session index under ~/.openclaw/workspace-memory-builder/.session_index/.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
