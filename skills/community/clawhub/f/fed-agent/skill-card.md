## Description:

Produces markdown summaries of Federal Reserve policy, interest rates, inflation metrics, and Fed speech notes using a bundled Python tracker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dimaschand29](https://clawhub.ai/user/dimaschand29)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts can use this skill to generate a local Federal Reserve policy summary for review in chat or console workflows. Outputs should be checked against authoritative public sources before use in economic, financial, or operational decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports that the skill presents static sample values as live Federal Reserve tracking.

Mitigation: Treat generated economic data as unverified until checked against Federal Reserve and BLS sources.

Risk: Documentation describes output options such as JSON, file saving, and data switches that are not implemented in the bundled script.

Mitigation: Review the artifact behavior before deployment and do not depend on undocumented command-line behavior without testing it.

## Reference(s):

- [Fed Agent ClawHub page](https://clawhub.ai/dimaschand29/skills/fed-agent)
- [Federal Reserve FOMC statements](https://www.federalreserve.gov/monetarypolicy/fomc.htm)
- [Federal Reserve money markets](https://www.federalreserve.gov/financialservices/moneymarket/index.htm)
- [BLS CPI inflation data](https://www.bls.gov/cpi/inflatedata.htm)
- [BLS employment data](https://www.bls.gov/emp/)
- [Federal Reserve speeches](https://www.federalreserve.gov/speeches/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown table with console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bundled static sample values; verify freshness and accuracy before relying on the output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
