## Description: <br>
Contract Doc Sync detects code-documentation drift and synchronizes local Contract-track Markdown docs under docs/modules, docs/architecture, and docs/conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leonardo-lb](https://clawhub.ai/user/leonardo-lb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill after code changes, before pull requests, and before releases to detect drift and update local Markdown documentation so it stays aligned with source code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads repository source, docs, build files, and agent guidance files to decide how documentation should change. <br>
Mitigation: Use it only in repositories where that local context is acceptable to expose to the agent, and prefer L0 or L1 for sensitive projects. <br>
Risk: L3 semantic consistency review can send code and documentation snippets to a cloud LLM provider. <br>
Mitigation: Set DOC_SYNC_SKIP_D10=true, use L0/L1, or use a local LLM when sensitive repository content must not leave the environment. <br>
Risk: Documentation edits can introduce inaccurate or overconfident statements when a change is semi-deterministic or creative. <br>
Mitigation: Review generated reports, inspect any [待确认] markers, and require explicit approval before accepting non-doc or human-confirmation changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/leonardo-lb/contract-doc-sync) <br>
- [Environment Probing](references/environment-probing.md) <br>
- [Sync Procedures](references/sync-procedures.md) <br>
- [Verification Dimensions Reference](references/verification-dimensions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown reports with JSON change summaries and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May edit whitelisted local Markdown documentation files and emit review markers for human confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
