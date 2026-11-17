## Description:

Course-ifies user-provided books into structured lessons and guides the learner through prep, Feynman-style teaching, practice gates, spaced review, recitation homework, and self-improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangyuan-3149](https://clawhub.ai/user/fangyuan-3149)

### License/Terms of Use:

MIT-0

## Use Case:

Readers, students, and developers use this skill to turn local PDF, EPUB, DJVU, MOBI, AZW, DOCX, text, Markdown, or CBZ books into a structured course and have an agent teach the material lesson by lesson. When explicitly authorized, the skill can also help locate and fetch public sources that the user is permitted to access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional web-acquisition path can run untrusted source rules and make broad network requests.

Mitigation: Prefer the local-book workflow; review the acquisition path before use and restrict fetching to user-confirmed public sources.

Risk: Imported source subscriptions or JavaScript-based source rules may introduce unsafe behavior.

Mitigation: Avoid untrusted source subscriptions and do not run online acquisition until JavaScript evaluation is sandboxed or removed.

Risk: Network acquisition can contact destinations outside the user's intended scope.

Mitigation: Enable TLS verification and restrict network destinations to confirmed public domains before using acquisition features.

## Reference(s):

- [Book Learning Tutor README](artifact/README.md)
- [Source Acquisition](artifact/references/source_acquisition.md)
- [Source Selection and Evaluation](artifact/references/source_selection.md)
- [Teaching Principles and Adaptive Strategy](artifact/references/teaching_patterns.md)
- [Self-Evolution Spec](artifact/references/self_evolution.md)
- [ClawHub Skill Page](https://clawhub.ai/fangyuan-3149/skills/book-learning-tutor)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown, structured course files, progress records, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Main local-book workflow writes course and learning-state files; optional online acquisition is authorization-gated.]

## Skill Version(s):

0.1.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
