## Description: <br>
Amber Hunter is a local AI memory engine that encrypts, stores, summarizes, retrieves, and optionally syncs OpenClaw and Claude Code session context and files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ankechenlab-node](https://clawhub.ai/user/ankechenlab-node) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use Amber Hunter to preserve long-running collaboration context as searchable local memory capsules, retrieve relevant past decisions, and compile related memories into wiki-style concept pages. It is intended for single-user local workflows with optional encrypted cloud sync through Huper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to continuously collect and reuse AI-session memory, including conversation context and recently modified files. <br>
Mitigation: Use it on a trusted single-user machine, review the privacy tradeoff before installation, and disable proactive capture for workspaces or sessions that should not be retained. <br>
Risk: Optional cloud sync can upload memory data to Huper, even though the artifact describes encryption before transmission. <br>
Mitigation: Avoid enabling cloud sync until the uploaded data and account configuration are understood; verify the master password and encryption settings before syncing sensitive memories. <br>
Risk: Server security evidence flags under-disclosed gaps around authentication and plaintext secrets, and the artifact notes a Bearer token stored on disk. <br>
Mitigation: Do not rely on the current token and secret handling for high-value credentials or DID keys; keep local token files protected and rotate credentials if exposure is suspected. <br>
Risk: The skill starts background services and includes scripts that can operate on memory data. <br>
Mitigation: Review installer, daemon, sync, and benchmark cleanup behavior before running them against real data; test destructive or cleanup flows only on disposable data. <br>


## Reference(s): <br>
- [Amber Hunter ClawHub Release](https://clawhub.ai/ankechenlab-node/amber-hunter) <br>
- [Amber Hunter README](artifact/README.md) <br>
- [Amber Hunter Skill Definition](artifact/SKILL.md) <br>
- [RAG Specification v1.2.41](artifact/docs/SPEC-RAG-v1.2.41.md) <br>
- [Knowledge Compiler Specification](artifact/docs/SPEC-knowledge-compiler-v1.0.md) <br>
- [Huper](https://huper.org) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance, shell command examples, JSON API responses, recall prompts, and compiled wiki-style Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local memory capsules, encrypted sync payloads, retrieved memory blocks, concept pages, and configuration changes.] <br>

## Skill Version(s): <br>
1.2.41 (source: server release metadata, artifact SKILL.md, CHANGELOG, and FastAPI app version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
