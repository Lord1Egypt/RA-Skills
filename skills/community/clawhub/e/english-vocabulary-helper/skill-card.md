## Description:

A bilingual English vocabulary learning helper for Chinese-speaking users that explains meanings, roots, affixes, usage examples, memory techniques, and generates Markdown notes plus interactive HTML study cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gratefulheart](https://clawhub.ai/user/gratefulheart)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and educators use this skill to study individual English vocabulary words with Chinese explanations, etymology, example sentences, memory aids, review cards, and quizzes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically creates persistent local Markdown and HTML files and opens generated HTML.

Mitigation: Review before installing and use only when local file creation and opening generated HTML are acceptable.

Risk: Vocabulary input could affect generated filenames or overwrite behavior.

Mitigation: Avoid untrusted word lists unless the skill is updated to sanitize filenames, stay within the vocabulary directory, avoid overwrites by default, and ask before saving or opening files.

## Reference(s):

- [Common English Roots Reference](artifact/references/common-roots.md)
- [Memory Techniques Guide](artifact/references/memory-techniques.md)
- [Vocabulary Output Template](artifact/references/output-template.md)
- [ClawHub Skill Page](https://clawhub.ai/gratefulheart/skills/english-vocabulary-helper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown vocabulary notes and interactive HTML study cards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent local vocabulary files and opens the generated HTML card for study.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
