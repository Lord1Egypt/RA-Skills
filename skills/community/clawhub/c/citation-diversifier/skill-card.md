## Description:

Generates a scope-safe citation budget report per H3 subsection so drafts can improve citation diversity and density without adding new facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willoscar](https://clawhub.ai/user/willoscar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and writing agents use this skill when a research draft is under-cited or failing a global unique-citation gate. It produces an in-scope citation budget that can guide later citation-injection edits without inventing citations or changing claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Path overrides can let untrusted command arguments or workspace metadata choose input and output locations outside the expected defaults.

Mitigation: Run only on trusted workspaces and prefer the default command without --inputs or --outputs until workspace-confined path handling is enforced.

Risk: The package includes broad pipeline and orchestration helper files beyond the narrow citation-budget workflow.

Mitigation: Review the bundled helper files before deployment and confirm they are intended for the release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/willoscar/skills/citation-diversifier)
- [ClawHub publisher profile](https://clawhub.ai/user/willoscar)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown report written to output/CITATION_BUDGET_REPORT.md, with status, citation targets, gap analysis, and per-H3 budget suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses existing workspace files such as output/DRAFT.md, outline/outline.yml, outline/writer_context_packs.jsonl, and citations/ref.bib; network access is not required.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
