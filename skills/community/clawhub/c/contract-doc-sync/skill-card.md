## Description:

Contract Doc Sync detects drift between code changes and contract-track Markdown documentation, then updates approved docs files and produces verification reports using local git and Markdown section tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonardo-lb](https://clawhub.ai/user/leonardo-lb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill after code changes, refactors, pull requests, and release preparation to check whether module, architecture, and convention documentation remains aligned with source behavior. It supports drift detection, scoped Markdown updates, and consensus-style verification of documentation consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run a project-provided Markdown section parser before falling back to its bundled parser.

Mitigation: Use the bundled parser or review any project-local md-sections script before execution.

Risk: Documentation updates may affect repository docs if write boundaries are not enforced by the agent runtime.

Mitigation: Restrict writes to docs/modules/*.md, docs/architecture/*.md, and docs/conventions/*.md and review proposed changes before committing.

Risk: L3 semantic verification may send code and documentation snippets to a cloud LLM provider.

Mitigation: Use L0 or L1 for sensitive repositories, use a local model, or set DOC_SYNC_SKIP_D10=true before L3 review.

## Reference(s):

- [Environment Probing](references/environment-probing.md)
- [Sync Procedures](references/sync-procedures.md)
- [Verification Dimensions Reference](references/verification-dimensions.md)
- [ClawHub Skill Page](https://clawhub.ai/leonardo-lb/skills/contract-doc-sync)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands, JSON change summaries, and proposed Markdown documentation edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Edits are intended to stay within docs/modules/*.md, docs/architecture/*.md, and docs/conventions/*.md; L0 reports only, while L1-L3 may propose or apply documentation updates depending on confidence.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
