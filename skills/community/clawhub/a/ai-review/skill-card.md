## Description:

Reads content from URLs or files, classifies it, and generates structured summaries and comments in a specific, analytical style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blackshady1130-jpg](https://clawhub.ai/user/blackshady1130-jpg)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn articles, papers, news, URLs, and local files into structured Markdown reviews with a classification, key takeaway, source details, and analytical commentary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports that the PDF workflow can expose users to command-injection and file-overwrite risk when handling untrusted links or paths.

Mitigation: Use structured, validated command arguments, secure temporary files, or a safer document parser before processing untrusted PDF URLs or paths.

Risk: The skill may access user-provided URLs or local files while preparing reviews.

Mitigation: Install and use it only when the agent is permitted to access the supplied sources, and avoid sensitive local paths unless they are needed for the review.

## Reference(s):

- [Style Guide: Opinion/Article](artifact/references/style_guide_article.md)
- [Style Guide: Solid Paper](artifact/references/style_guide_paper.md)
- [Style Guide: Industry News/Commentary](artifact/references/style_guide_industry.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single table row containing type, date, title, source, key takeaway, and comments.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
