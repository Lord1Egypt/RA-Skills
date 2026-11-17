## Description:

Runs a preliminary customer compliance background check by guiding OFAC sanctions searches, BIS/ECFR address keyword checks, and drafting an internal export-data coordination request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kittymi](https://clawhub.ai/user/kittymi)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or compliance operators use this skill to perform an initial customer sanctions and blacklist screening workflow, summarize unresolved matches, and prepare a coordination message for export-data review. It supports triage and documentation, not final legal or compliance determinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Potential OFAC or ECFR matches can be false positives or incomplete due to keyword choice and source-page behavior.

Mitigation: Review candidate names, addresses, entity types, scores, and page context manually before treating any result as a compliance finding.

Risk: The drafted Dora or Shellen coordination message may be sent before export-data facts are verified.

Mitigation: Require user confirmation before sending the message and keep the result labeled as a request or draft until a human response is received.

Risk: A no-result search can be mistaken for a final compliance clearance.

Mitigation: Frame clean searches as preliminary non-matches for the tested keywords and keep information gaps visible in the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kittymi/skills/customer-background-check)
- [Publisher profile](https://clawhub.ai/user/kittymi)
- [OFAC Sanctions List Search](https://sanctionssearch.ofac.treas.gov/)
- [ECFR Supplement No. 4 to Part 744](https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-744/appendix-Supplement%20No.%204%20to%20Part%20744)
- [Customer background check quick checklist](references/checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with screening results, open questions, and a drafted coordination message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires manual review of potential OFAC or ECFR matches and user confirmation before any drafted message is sent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
