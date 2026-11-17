## Description:

Hybrid search memory system for AI agents. Manual search and storage - auto-capture is opt-in only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hargabyte](https://clawhub.ai/user/hargabyte)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI agents use Chaos Mind to search, store, and review local project or team memories before, during, and after work. Optional auto-capture can extract decisions, facts, and insights from explicitly configured session transcript paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads release binaries and supports a curl-to-shell installation path, which creates supply-chain review risk.

Mitigation: Review install.sh before execution, avoid curl-to-shell where practical, and independently verify release provenance or hashes for downloaded binaries.

Risk: The optional background consolidator service can persist and process configured files over time.

Mitigation: Prefer one-shot or user-level operation until the service file and runtime behavior are reviewed; enable the system-wide service only when needed.

Risk: Auto-capture can read session transcripts from configured paths and store extracted memories locally.

Mitigation: Keep auto-capture disabled until the exact transcript paths are reviewed, use dry-run or one-shot mode first, and configure only intended sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hargabyte/skills/chaos-mind)
- [Publisher Profile](https://clawhub.ai/user/hargabyte)
- [CHAOS Memory Repository](https://github.com/hargabyte/Chaos-mind)
- [README](https://github.com/hargabyte/Chaos-mind/blob/main/README.md)
- [Security Policy](https://github.com/hargabyte/Chaos-mind/blob/main/SECURITY.md)
- [Installation Notes](https://github.com/hargabyte/Chaos-mind/blob/main/INSTALL_NOTES.md)
- [Ollama](https://ollama.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result detail can be selected with index, summary, or full modes; auto-capture remains opt-in.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
