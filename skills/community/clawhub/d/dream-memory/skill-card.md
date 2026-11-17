## Description:

Dream Memory guides agents through a four-layer workspace memory system using Markdown files, OpenViking vector indexing, Ollama bge-m3 embeddings, and session lifecycle rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shoukuan](https://clawhub.ai/user/shoukuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install, operate, and troubleshoot a persistent workspace memory system with daily logs, long-term memory promotion, vector retrieval, and session start/end checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance includes piping a downloaded Ollama installer directly to sh.

Mitigation: Use a reviewed package-manager install path or inspect and verify the installer before execution.

Risk: The OpenViking example enables broad CORS with wildcard origins.

Mitigation: Restrict CORS to trusted local origins or disable cross-origin access when it is not needed.

Risk: The memory system persists and indexes workspace, home-directory, and session metadata.

Mitigation: Enable it only for workspaces where persistent memory is acceptable, and avoid storing secrets or sensitive personal data in memory files.

## Reference(s):

- [Ollama + OpenViking setup](references/ollama-setup.md)
- [ClawHub skill page](https://clawhub.ai/shoukuan/skills/dream-memory)
- [Ollama installer](https://ollama.com/install.sh)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a shell self-check script and configuration guidance for local Ollama, OpenViking, and OpenClaw memory search.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
