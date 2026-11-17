## Description:

Create a three-tier HOT/WARM/COLD memory directory structure for OpenClaw agents and provide configuration guidance for Gemini Embeddings 2 semantic memory search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autosolutionsai-didac](https://clawhub.ai/user/autosolutionsai-didac)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to initialize an OpenClaw workspace with structured memory files and to configure semantic memory search using Google Gemini embeddings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory file content may be sent to Google Gemini when semantic search is enabled.

Mitigation: Enable Gemini-backed memory search only for workspaces whose memory contents are appropriate to send to Google Gemini, and keep sensitive material out of indexed memory files when that is not acceptable.

Risk: The optional Lossless Claw plugin is installed separately and is third-party software.

Mitigation: Review and pin the optional plugin before installing it in an agent workspace.

Risk: The setup script writes starter memory files into the target workspace.

Mitigation: Run the script only against the intended workspace path and review existing memory files before setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autosolutionsai-didac/skills/agent-memory-setup-v2)
- [Google AI Studio API key setup](https://aistudio.google.com/apikey)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included setup script creates memory directories and starter files when run by the user.]

## Skill Version(s):

1.0.4 (source: ClawHub server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
