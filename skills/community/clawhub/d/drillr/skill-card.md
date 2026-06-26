## Description: <br>
Power terminal for deep financial research on US public equities — reason through investment theses, screen for ideas, map supply chains, do forensic accounting, pull earnings call quotes, model financials, and more in plain English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yx9966](https://clawhub.ai/user/yx9966) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External financial researchers, analysts, and investors use this skill to ask natural-language questions about US public equities, including screens, SEC filing lookup, earnings call analysis, peer tables, valuation work, event research, and financial modeling support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User prompts are sent to the drillr external API. <br>
Mitigation: Do not include secrets, credentials, account-specific data, or nonpublic business information in prompts. <br>
Risk: Financial research output may contain incorrect or stale investment-relevant facts. <br>
Mitigation: Verify material figures, quotes, and conclusions against primary sources such as SEC filings and earnings materials before relying on them. <br>


## Reference(s): <br>
- [drillr homepage](https://drillr.ai) <br>
- [ClawHub skill page](https://clawhub.ai/yx9966/drillr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with optional markdown tables printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Streams Server-Sent Events from a single external API request; queries are capped at 8 KB.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
