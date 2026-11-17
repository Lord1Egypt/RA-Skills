## Description:

Remove AI-like features from Chinese and English text to make it more natural and human-like.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youstudyeveryday](https://clawhub.ai/user/youstudyeveryday)

### License/Terms of Use:

MIT

## Use Case:

External users, content editors, and developers use this skill to detect AI-like phrasing and rewrite Chinese or English text in natural, casual, or formal styles. Results should be reviewed before publication to preserve meaning and meet authorship disclosure expectations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processed output may overwrite files when users point output paths at existing originals.

Mitigation: Use separate output directories, keep originals unchanged, and review processed files before replacing source material.

Risk: Text rewriting can change meaning, tone, or disclosure expectations for AI-assisted content.

Mitigation: Review results before publishing and disclose AI assistance where required by policy, platform rules, or law.

Risk: The optional jieba dependency affects Chinese text processing and is not pinned by the artifact documentation.

Mitigation: Pin and review the jieba package version before installation in controlled environments.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/youstudyeveryday/skills/deai-skill)
- [Declared project homepage](https://github.com/yourusername/deai-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can report AI feature scores and detected phrases; CLI use can write processed text to output files.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
