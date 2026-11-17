## Description:

Doc Gap Finder scans documentation directories, heading structures, and file distribution to identify missing sections, duplicate content, and stale areas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation maintainers, and knowledge-base owners use this skill to audit local documentation before cleanup or release. It produces a directory overview, suspected gaps, duplicate or near-duplicate sections, suggested additions or deletions, and priorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive local documentation if pointed at broad personal, private, or credential-containing directories.

Mitigation: Provide narrow documentation paths, prefer dry-run or stdout review for sensitive repositories, and avoid scanning unrelated personal or credential directories.

Risk: Audit suggestions can be incomplete or misleading if the sampled documents are sparse, outdated, or outside the intended documentation scope.

Mitigation: Review generated gaps, duplicate findings, and deletion suggestions before changing source documents or publishing results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/doc-gap-finder)
- [Skill manifest](artifact/SKILL.md)
- [README](artifact/README.md)
- [Output specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Structured Markdown report by default, with an optional JSON wrapper from the support script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Python support script accepts input path, output path, format, limit, and dry-run options.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
