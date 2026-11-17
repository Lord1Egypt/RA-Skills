## Description:

Designs, audits, or executes user-requested historical-folder modernization into privacy-aware, reviewable Agent Assets for a personal second brain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lee-agi](https://clawhub.ai/user/lee-agi)

### License/Terms of Use:

Apache-2.0 OR MIT-0

## Use Case:

Developers, operators, and knowledge workers use this skill to inventory mixed historical folders, convert safe material into `.agent.md` entries, review retention decisions, and build final non-PII retrieval indexes after explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File movement, review application, synchronization, deletion, and indexing can affect local workspaces when execution gates are enabled.

Mitigation: Start with plan-only or dry-run stages, inspect generated decisions and path effects, and use `--execute-*` flags only after explicit approval.

Risk: Long-term synchronization can continue watching selected directories after setup.

Mitigation: Enable LaunchAgent sync only for directories intended to be watched long term, monitor sync status, and disable the watcher when it is no longer needed.

Risk: Optional provider-backed summary or embedding features may send bounded query or index text to a remote provider.

Mitigation: Use remote summary or embedding settings only with an approved provider and require separate opt-in for semantic reranking.

Risk: Generated indexes, logs, review decisions, personal source material, or absolute user paths could expose private workspace context if distributed.

Mitigation: Keep runtime output outside the installed skill package and exclude credentials, generated indexes, personal notes, local logs, and absolute paths from reports or releases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lee-agi/skills/agent-os-asset)
- [README](README.md)
- [Security boundaries and migration](references/security-boundaries.md)
- [Agent Readable Doc Conversion Workflow](skills/agent-readable-doc/references/conversion-workflow.md)
- [KB Review Workflow](skills/kb-review/references/workflow.md)
- [KB Review Output Specification](skills/kb-review/references/output-spec.md)
- [Second Brain Privacy Rules](skills/second-brain/references/privacy.md)
- [Agent Asset Federation](skills/second-brain/references/asset-index-federation.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and shell command guidance with generated local asset files and indexes when explicitly enabled]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-first outputs are staged behind review, privacy, and explicit execution gates; optional provider-backed reranking can transmit bounded query or index text only after separate approval.]

## Skill Version(s):

0.2.0 (source: SKILL.md frontmatter, package.json, pyproject.toml, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
