## Description:

Summarize, analyze, and extract insights from local text documents without external APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and knowledge workers use this skill to digest reports, extract ranked bullets and keywords, compute readability statistics, detect outlines, and compare two document versions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads document files supplied by the user, so sensitive content in those files may be processed locally by the agent workflow.

Mitigation: Run it only on documents the user intentionally selects for analysis and review the selected paths before execution.

Risk: Server security guidance notes a functional quoting issue around file arguments that may affect reliability.

Mitigation: Test commands on non-sensitive sample files before relying on results for important document review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/skills/bytesagain-doc-summarizer)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with command examples and document analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local summaries, bullets, keyword tables, statistics, outlines, and document comparison results from user-specified files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
