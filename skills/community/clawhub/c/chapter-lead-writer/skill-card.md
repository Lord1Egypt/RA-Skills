## Description:

Writes body-only H2 chapter lead blocks that preview a chapter's comparison lens and connect its H3 subsections without adding new facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willoscar](https://clawhub.ai/user/willoscar)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and research agents use this skill to generate short chapter lead files for H2 sections that have multiple H3 subsections. It is intended for literature-review and long-form research workspaces where leads must stay within existing chapter facts and citation scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes broader research-pipeline routing and orchestration files beyond the advertised chapter-lead writer.

Mitigation: Install it only where the bundled research-pipeline files are acceptable; for the narrow lead-writing behavior, configure the agent environment to load only the necessary skill entry point and runner.

Risk: The runner mutates workspace files by writing chapter lead files and a chapter-leads report.

Mitigation: Run it only against a reviewed workspace, then inspect generated files under sections/ and output/ before accepting the changes.

Risk: Generated leads can be misleading if chapter briefs or citation scope are incomplete.

Mitigation: Confirm outline/chapter_briefs.jsonl and citations/ref.bib are current, and review each lead against downstream chapter content before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/willoscar/skills/chapter-lead-writer)
- [Overview](references/overview.md)
- [Lead Block Archetypes](references/lead_block_archetypes.md)
- [Throughline Patterns](references/throughline_patterns.md)
- [Bridge Examples](references/bridge_examples.md)
- [Bad Narration Examples](references/bad_narration_examples.md)
- [Lead Block Contract](assets/lead_block_contract.json)
- [Lead Block Compatibility Defaults](assets/lead_block_compatibility_defaults.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown files and a Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes body-only lead files under sections/S<sec_id>_lead.md and a workspace report at output/CHAPTER_LEADS_REPORT.md.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
