## Description:

Review federal exclusion evidence for a business or person using GovGazette when the user asks about a potential SAM exclusion, debarment or suspension match. Built by Moosh Works (https://mooshworks.com).

This skill is ready for commercial/non-commercial use.

## Publisher:

[mooshee](https://clawhub.ai/user/mooshee)

### License/Terms of Use:

MIT-0

## Use Case:

People reviewing a possible federal exclusion, debarment, or suspension match can use this skill to look up public records, assess identity evidence, and summarize dated source details. It supports review and citation of records but does not determine eligibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Names or identifiers submitted for a lookup may expose information to an external service.

Mitigation: Use identifiers supplied by the user or established in an official source; keep credentials and confidential bid material out of queries.

Risk: Similar names or conflicting identifiers can yield a potential match that does not establish identity or current exclusion status.

Mitigation: Report identity evidence, source status, dates, and official links; verify potential matches against dated official records and do not make an eligibility determination.

## Reference(s):

- [GovGazette](https://govgazette.com)
- [GovGazette MCP endpoint](https://govgazette.com/mcp)
- [ClawHub release page](https://clawhub.ai/mooshee/skills/exclusion-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summary with identity evidence, record details, dates, and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes citations to returned records and dated official sources; no-match results are not clearance.]

## Skill Version(s):

1.3.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
