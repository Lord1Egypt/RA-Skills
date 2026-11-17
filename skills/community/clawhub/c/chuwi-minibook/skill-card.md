## Description:

A Chuwi Minibook utility skill documented for system status checks; release security evidence notes that the packaged behavior instead searches local knowledge and insight-history data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can invoke this skill for Chuwi Minibook-related local search results or, according to its documentation, system status summaries. Review fit carefully because release security evidence reports a mismatch between the documented monitoring behavior and the packaged code behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented system-monitoring behavior does not match the packaged behavior reported by release security evidence.

Mitigation: Review the skill before installation and describe it to users as a local knowledge/history search skill unless the implementation is changed to match the monitoring documentation.

Risk: The packaged code can read shared local knowledge/history data and import Python code from an external database directory.

Mitigation: Install only in trusted workspaces, restrict access to the shared database directory, and review that directory before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/chuwi-minibook)
- [Publisher profile](https://clawhub.ai/user/534422530)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON object with status, topic, query, count, result records, and timestamp]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include locally sourced knowledge-base or insight-history entries when available.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
