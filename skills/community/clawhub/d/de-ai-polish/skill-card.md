## Description:

Detects AI-like patterns in Chinese writing and helps agents produce issue reports, edit suggestions, revised natural text, and quality scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cat-xierluo](https://clawhub.ai/user/cat-xierluo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and writing agents use this skill to review Chinese articles, reports, speeches, and public posts for AI-like phrasing, mechanical structure, empty summaries, over-polished transitions, punctuation issues, and unnatural rhythm. It supports detection reports, problem-type labels, concrete delete/merge/rewrite suggestions, revised text, and follow-up quality scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tries to make itself a mandatory pre-output step for writing workflows.

Mitigation: Use it as an explicit opt-in review step for Chinese writing rather than a global mandatory gate.

Risk: Fix workflows can overwrite article files.

Mitigation: Keep original drafts, write changes to a copy when possible, and review diffs before accepting edits.

Risk: Style polishing can alter author intent or remove useful legal, technical, or fixed expressions.

Mitigation: Compare revised text with the source draft and preserve necessary terminology, citations, quotes, and factual claims.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cat-xierluo/skills/de-ai-polish)
- [Publisher Profile](https://clawhub.ai/user/cat-xierluo)
- [Legal Skills Repository Homepage](https://github.com/cat-xierluo/legal-skills)
- [Expression Transformations](reference/expression-transformations.md)
- [Personal Style Guide](reference/personal-style-guide.md)
- [Quality Scoring](reference/quality-scoring.md)
- [Sentence Rhythm Guide](reference/sentence-rhythm-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports and revised Chinese text, with optional shell commands for punctuation normalization]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May revise or overwrite article files when fix workflows are used; review diffs before accepting changes.]

## Skill Version(s):

1.4.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
