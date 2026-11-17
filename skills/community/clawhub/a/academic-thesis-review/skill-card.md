## Description:

Multi-round review skill for Chinese management-oriented master's theses, especially MBA, MEM, and MPA, with applicability to similar professional and applied research theses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wmpluto](https://clawhub.ai/user/wmpluto)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to review Chinese master's thesis drafts or revised versions and produce structured Chinese revision feedback across macro, chapter-level, and cross-chapter checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill saves extracted thesis text, working notes, and review results on disk, which may expose sensitive or unpublished thesis content.

Mitigation: Run it in a dedicated working folder, control access to review_artifacts and review_results.md, and review generated artifacts before sharing.

Risk: Automated thesis review can produce incorrect or overly strong academic recommendations.

Mitigation: Treat findings as revision guidance and manually verify suspicion or manual-check items against the original Word file, source literature, and external facts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wmpluto/skills/academic-thesis-review)
- [Skill Repository](https://github.com/wmpluto/academic-thesis-review-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance, Files]

**Output Format:** [Markdown reports, plain-text extraction artifacts, and inline Python or shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates review_results.md and timestamped review_artifacts files in the working directory.]

## Skill Version(s):

1.1.0 (source: server release metadata, SKILL.md frontmatter, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
