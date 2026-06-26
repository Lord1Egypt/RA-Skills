## Description: <br>
ClawVault gives OpenClaw agents local structured memory with graph-aware retrieval, checkpoint and recovery workflows, semantic search, observational memory, and optional hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G9Pedro](https://clawhub.ai/user/G9Pedro) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use ClawVault to persist, retrieve, and inject local agent memory across OpenClaw sessions, checkpoint work, recover context, and repair broken session transcripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory and enabled hooks can automatically reuse past session and vault context in future agent prompts. <br>
Mitigation: Review the hook before enabling it, choose the vault path deliberately, and avoid storing secrets or unrelated private history in the vault. <br>
Risk: Transcript-derived content can be sent to Gemini when observe compression is used with GEMINI_API_KEY configured. <br>
Mitigation: Leave GEMINI_API_KEY unset unless sending transcript-derived content to Gemini is acceptable for the work. <br>
Risk: Session repair workflows can modify OpenClaw session transcripts. <br>
Mitigation: Use dry-run review before repair when possible and rely on the documented automatic backups before accepting transcript changes. <br>


## Reference(s): <br>
- [ClawVault on ClawHub](https://clawhub.ai/G9Pedro/clawvault) <br>
- [ClawVault homepage](https://clawvault.dev) <br>
- [ClawVault npm package](https://www.npmjs.com/package/clawvault) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [qmd dependency](https://github.com/tobi/qmd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI command examples, environment variable names, hook behavior descriptions, and local context bullets when enabled.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local vault files, register opt-in OpenClaw hooks, and reuse vault context in future agent prompts.] <br>

## Skill Version(s): <br>
2.5.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
