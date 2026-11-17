## Description:

Summarize lengthy plain text into a concise TL;DR and 3-5 key bullet points, preserving important names, dates, and figures verbatim.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers can use this skill to turn long plain-text articles or documents into a concise TL;DR and 3-5 key takeaways while preserving important names, dates, and figures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled TaskFlow workflow can publish the whole skill directory to ClawHub using runner credentials.

Mitigation: Review the workflow before execution and run it only in an environment with ClawHub publishing credentials when publishing the reviewed directory contents is intended.

Risk: LLM-generated summaries can omit or misstate important details from the source text.

Mitigation: Review summaries against the original text for high-impact use cases and preserve names, dates, and figures exactly as instructed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/demo-text-summarizer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with a TL;DR sentence and 3-5 key bullet points]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves important names, dates, and figures verbatim when summarizing.]

## Skill Version(s):

1.0.0 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
