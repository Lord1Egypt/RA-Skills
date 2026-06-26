## Description: <br>
Agent memory system with graph-aware context profiles, checkpoint/recover, semantic search, and structured markdown storage for managing session knowledge locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to store and retrieve agent memories, checkpoint work, recover context after interrupted sessions, and configure OpenClaw memory workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on external CLI and hook code that was not included in the reviewed artifact. <br>
Mitigation: Inspect the installed npm package and OpenClaw hook handler locally before enabling hooks, and pin package versions where possible. <br>
Risk: Persistent hooks and repair workflows can access or modify OpenClaw session transcripts. <br>
Mitigation: Enable hooks only after review, keep backups enabled for transcript repair, and run diagnostics before relying on runtime integration. <br>
Risk: Memory files and transcript observations may contain sensitive information. <br>
Mitigation: Set an explicit CLAWVAULT_PATH, avoid storing secrets in memories, and use compression only for transcripts that may be sent to the configured LLM provider. <br>


## Reference(s): <br>
- [ClawVault homepage](https://clawvault.dev) <br>
- [ClawVault npm package](https://www.npmjs.com/package/clawvault) <br>
- [qmd dependency](https://github.com/tobi/qmd) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local markdown memory files and OpenClaw hook configuration when the referenced CLI and hooks are installed and run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.5.11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
