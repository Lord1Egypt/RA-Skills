## Description:

Generate word frequency statistics and word cloud from social media comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dkgee](https://clawhub.ai/user/dkgee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operators use this skill to process social media comment JSON, identify frequent terms, and create a word cloud for topic analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency drift can change tokenization or word cloud rendering behavior.

Mitigation: Install in an isolated virtual environment and pin jieba, wordcloud, and matplotlib versions.

Risk: Running the script in a shared or important directory can overwrite existing word_freq.json or word_cloud.png files.

Mitigation: Use a dedicated output directory for each run and preserve any prior outputs before reusing the directory.

Risk: The script processes local comment JSON that may contain sensitive or unintended data.

Mitigation: Run it only on comment files intended for this analysis.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dkgee/skills/comment-wordcloud)
- [Sample Comments JSON](artifact/references/sample_comments.json)
- [Stop Words List](artifact/references/stop_words.txt)

## Skill Output:

**Output Type(s):** [Files, JSON, Images, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands; generated artifacts are JSON and PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or overwrites word_freq.json and word_cloud.png in the selected output directory.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
