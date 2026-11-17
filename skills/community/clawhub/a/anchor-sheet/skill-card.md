## Description:

Extracts per-subsection anchor facts from evidence packs so writers include concrete numbers, benchmarks, and limitations instead of generic summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willoscar](https://clawhub.ai/user/willoscar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and writing agents use Anchor Sheet in evidence-based research-writing workspaces to convert `outline/evidence_drafts.jsonl` and `citations/ref.bib` into citation-backed anchor facts for each H3 subsection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unchecked command-line input paths could read or overwrite files outside the intended workspace.

Mitigation: Run only in a contained workspace and use workspace-relative `--inputs` and `--outputs` values without absolute paths or `../` segments.

Risk: The package includes broad workflow code beyond the anchor-sheet script.

Mitigation: Review the bundled files before installation and prefer a tightened package containing only the anchor-sheet script and declared workspace files.

Risk: Untrusted workspace files such as `UNITS.csv` or pipeline metadata could influence execution paths.

Mitigation: Use trusted workspace inputs and inspect generated outputs before downstream writing or publication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/willoscar/skills/anchor-sheet)
- [Publisher Profile](https://clawhub.ai/user/willoscar)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSONL file plus Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes `outline/anchor_sheet.jsonl` with one object per H3 subsection.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
