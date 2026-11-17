## Description:

Short alias for content-search-summarization. Use this to search public content platforms, rank the top relevant items, and summarize them with links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allens0104](https://clawhub.ai/user/allens0104)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and content analysts use this skill to search public content platforms such as Bilibili or YouTube, rank relevant results, and produce concise summaries with source links, capture context, confidence notes, and caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic summary requests may accidentally activate public content search behavior.

Mitigation: Invoke the skill explicitly, such as with `/content-summary`, when platform search and metadata-based summaries are desired.

Risk: Summaries may be based on public page metadata rather than full content review.

Mitigation: Include confidence labels, source links, capture context, and clear caveats when summaries are metadata-inferred.

Risk: The referenced detailed playbook may not exist in the user's environment.

Mitigation: Verify that the separate content-search-summarization playbook is available before relying on alias behavior.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Structured Markdown with ranked links, summaries, confidence labels, and caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes search method, keyword and capture scope, source links, capture time when visible, and an explicit note when summaries are inferred from metadata.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
