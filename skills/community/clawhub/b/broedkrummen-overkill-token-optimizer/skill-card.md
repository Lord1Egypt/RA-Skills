## Description: <br>
Optimizes OpenClaw agent token usage with CLI compression, session indexing, local session search, reset support, and token usage checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Broedkrummen](https://clawhub.ai/user/Broedkrummen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw agent users use this skill to inspect token usage, compress command output, index prior sessions, search local session memory, and reset large sessions when managing context size. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external oktk CLI for compression. <br>
Mitigation: Install oktk only from trusted sources, preferably npm or verified releases. <br>
Risk: The index and search commands can make local OpenClaw session memory searchable on disk. <br>
Mitigation: Index only session memory suitable for local search and delete ~/.openclaw/workspace-memory-builder/.session_index when the retained index is no longer needed. <br>
Risk: The compress command runs user-selected shell commands through the external CLI. <br>
Mitigation: Use token-optimizer compress only with commands you intended to run and review command effects before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Broedkrummen/broedkrummen-overkill-token-optimizer) <br>
- [Publisher profile](https://clawhub.ai/user/Broedkrummen) <br>
- [oktk CLI repository](https://github.com/satnamra/oktk) <br>
- [Skill instructions](SKILL.md) <br>
- [Framework notes](FRAMEWORK.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or search a local session index under ~/.openclaw/workspace-memory-builder/.session_index.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
