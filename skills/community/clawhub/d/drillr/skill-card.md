## Description:

Power terminal for deep financial research on US public equities — reason through investment theses, screen for ideas, map supply chains, do forensic accounting, pull earnings call quotes, model financials, and more in plain English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yx9966](https://clawhub.ai/user/yx9966)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to ask plain-English financial research questions about US public equities, including screening, filing lookup, earnings call quote retrieval, peer comparisons, forensic accounting, and financial modeling support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented inline invocation can turn a crafted user question into locally executed Python code.

Mitigation: Prefer the companion query.py script with the question passed as an argument, or fix and review the inline invocation before use.

Risk: Each research question is sent to the drillr.ai public API endpoint.

Mitigation: Avoid sending confidential, personal, or restricted financial research prompts unless the endpoint and data handling are approved for that use.

Risk: The API returns AI-generated financial research that may contain incorrect figures or interpretations.

Mitigation: Verify material figures and conclusions against primary SEC filings, company disclosures, or other authoritative sources before acting on them.

## Reference(s):

- [drillr homepage](https://drillr.ai)
- [ClawHub skill page](https://clawhub.ai/yx9966/skills/drillr)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown text printed to stdout, with generated tables rendered as markdown when returned by the API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The companion script caps queries at 8 KB, sends one HTTPS POST to the public drillr API, streams SSE responses, and does not persist local state.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
