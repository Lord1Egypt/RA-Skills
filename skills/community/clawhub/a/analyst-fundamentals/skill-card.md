## Description:

Analyzes A-share company fundamentals from a stock code by gathering Eastmoney F10 data and synthesizing structured research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vbdspd](https://clawhub.ai/user/vbdspd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to produce structured fundamental-analysis research for Chinese A-share companies from a supplied stock code. It is intended for informational analysis, not personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow performs broad scraping and contacts Eastmoney.

Mitigation: Run it only where external access to Eastmoney is expected and allowed.

Risk: The skill creates many local analysis files.

Mitigation: Use it only in a workspace where creating and retaining those files is acceptable.

Risk: Generated analysis may include recommendation-like or position-sizing language despite the no-advice purpose.

Mitigation: Treat outputs as informational research and review them before relying on them.

Risk: Unvalidated stock-code input could drive unexpected requests or file paths.

Mitigation: Validate stock codes to a strict six-digit format before running the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vbdspd/skills/analyst-fundamentals)
- [Publisher profile](https://clawhub.ai/user/vbdspd)
- [Eastmoney F10 data source](https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown reports and structured analysis files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces multiple intermediate Markdown analysis files and a final report for the requested stock code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
