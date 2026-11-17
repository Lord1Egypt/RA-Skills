## Description:

Retrieves transcripts for videos on Instagram, LinkedIn, Meta Ad Library, Reddit, TikTok, X, and YouTube and presents them in a table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can provide video links and retrieve available transcripts for review, analysis, or later summarization by their agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplied video URLs are sent to DataXAPI, and retrieved transcripts are saved locally.

Mitigation: Avoid confidential or token-bearing links, and store transcript files where their contents can be handled appropriately.

Risk: Transcript calls can incur per-video charges.

Mitigation: Review the plan and maximum charge before execution, set an explicit spend cap, and use an API key with a limited budget.

Risk: The external CLI and service behavior are outside the supplied artifact review.

Mitigation: Use a reviewed, pinned CLI version.

## Reference(s):

- [DataXAPI Skills](https://dataxapi.com/skills/)

## Skill Output:

**Output Type(s):** [Files, Text, Guidance]

**Output Format:** [CSV transcript file with Markdown and command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts up to 10 video links per run; returns available transcripts with link, language, and text, while links without transcripts are omitted.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
