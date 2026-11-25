## Description:

Verify that example commands and their documented outputs in a technical document, tutorial, README, or skill package are actually reproducible. Use this when a doc contains runnable command examples, before publishing a doc or package whose examples must be trustworthy, when you need to change sample data inside a document (e.g. de-identify real birth dates, account numbers, or customer names) without introducing false claims, or when a document claims a script emits specific fields/values and you need to confirm it does. Covers: extracting every runnable example, separating mutable sample data from immutable factual tables, re-deriving every claimed value by actually running the tool instead of computing it by hand, bulk replacement with a change-count audit trail, and a per-example PASS/FAIL regression run. Trigger phrases: 'verify the examples in this doc', 'are these commands still correct', 'check the doc examples', 'replace the sample data in the docs', 'the docs claim X, does it really output X'.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to check that runnable examples match current tool behavior, safely revise sample data without changing factual content, and record per-example regression results before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One reference in the skill could not be resolved, leaving its relevance uncertain.

Mitigation: Review what the unresolved reference supports before installing or relying on the skill.

Risk: Example commands and bulk replacements can execute commands or change document files.

Mitigation: Run commands with write or delete effects in an isolated copy, then inspect the resulting files and change report.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/haiyangchenbj/skills/doc-example-reproducibility-check)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands]

**Output Format:** [Markdown checklists, example command results, and PASS/FAIL audit summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include per-example results, change counts, and a list of factual data intentionally left unchanged.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
