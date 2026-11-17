## Description:

Generates a client-facing executive KPI dashboard from QuickBooks Online data as an Excel workbook with traffic-light scoring, 6-month trend sparklines, watch items, and a month-over-month CDC log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External accounting and advisory teams use this skill after monthly close to generate executive KPI dashboard workbooks for clients with QuickBooks Online integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Client financial data may be written to local workbooks or the CDC cache in unintended locations.

Mitigation: Run only in an environment approved for client financial data, choose a restricted output directory, and review or clear the CDC cache according to retention policy.

Risk: Unpinned local dependencies can change reporting behavior across runs.

Mitigation: Use a dedicated virtual environment with pinned dependencies before running the pipeline.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/client-dashboard)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands; generated artifact is an Excel workbook]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates KPI_Dashboard_{slug}_{YYYY_MM}.xlsx and a local CDC cache at .cache/client-dashboard/{slug}.json.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
