## Description:

Counts, splits, and recombines oversized LinkedIn Sales Navigator searches, then loads them into a small set of Cargo models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales operations and GTM engineering teams use this skill to extract account or people result sets that exceed Sales Navigator's per-search limit. It guides them through counting and splitting searches, removing duplicates, and loading results into Cargo models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Large extractions and repeated people searches can consume additional credits.

Mitigation: Review the expected rows and credit estimate, test a small search, and approve the full extraction before running it.

Risk: The external Cargo CLI and optional skills bundle were not included for inspection.

Mitigation: Review their versions and contents separately before use.

## Reference(s):

- [Cargo GTM Skills project homepage](https://github.com/getcargohq/gtm-skills)
- [ClawHub release page](https://clawhub.ai/cargo-ai/skills/extract-sales-navigator-search)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell command examples and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
