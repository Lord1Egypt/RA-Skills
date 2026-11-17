## Description:

企业查询助手(免费版) helps agents perform Chinese-language company lookups for basic company information, shareholders, legal representatives, external investments, and business registration changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and business teams can use this skill to query company records and format structured lookup results for everyday company background checks. It is not presented as a full due-diligence, risk-screening, batch-query, or monitoring solution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs Node-based commands for company lookups and requests broad command and file authority.

Mitigation: Install only in an environment where command execution is acceptable, review commands before running them, and keep execution scoped to the documented lookup workflow.

Risk: Company or person identifiers may be sent to an external business-information API.

Mitigation: Avoid submitting sensitive due-diligence subjects or confidential identifiers unless the API provider and data handling terms are clarified.

Risk: The evidence flags unclear or conflicting SEO, generic file-processing, and risk-screening claims.

Mitigation: Treat the company lookup functions as the supported scope and avoid relying on unresolved claims for sensitive due-diligence, SEO, or risk-screening workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/company-search-tool-free)
- [Detailed reference](artifact/references/detail.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell and Python examples, plus structured JSON or text results from lookup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language interaction; Node.js command execution; company and person identifiers may be sent to an external business-information API.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
