## Description:

Search the web with EmpirioLabs AI and get current results, one answer with its sources, or a research report with citations. Use when the user asks to look something up online, to find recent news, documentation, or sources, to answer a question with citations, or to research a topic in depth. Runs a bundled Python script that picks a search model from the live catalog (or the one you name) and prints the results or saves them to the path you choose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[empiriolabs](https://clawhub.ai/user/empiriolabs)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to look up current information, get answers with sources, and prepare cited research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A partial security review flagged possible exposure of EMPIRIOLABS_API_KEY if an automatic redirect sends it to a different host; the available evidence is incomplete.

Mitigation: Review redirect handling before use, and use a dedicated key with limited account exposure until its behavior is understood; rotate the key if exposure is suspected.

## Reference(s):

- [EmpirioLabs AI documentation](https://docs.empiriolabs.ai)
- [EmpirioLabs AI MCP setup](https://docs.empiriolabs.ai/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files]

**Output Format:** [Search results or sourced answers as text; research reports as Markdown; full results as JSON when requested; optional saved output file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include source URLs and, for research reports, citations; output can be saved to a chosen path.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
