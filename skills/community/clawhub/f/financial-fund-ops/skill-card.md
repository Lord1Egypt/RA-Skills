## Description:

Fund administration and finance operations skill for GL reconciliation, break tracing, accrual schedules, roll-forwards, variance commentary, and NAV statement tie-out.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Fund administration and finance operations teams use this skill to prepare reconciliation outputs, investigate breaks, draft accrual schedules, build close-package roll-forwards, write variance commentary, and check LP statement NAV tie-outs for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft journal entries, break classifications, variance drivers, or NAV flags may be incomplete or incorrect if the supplied finance data or policies are incomplete.

Mitigation: Treat outputs as review drafts and require controller, resolver, or publisher approval before posting entries, changing statements, or taking operational action.

Risk: The skill may read sensitive fund administration data such as GL, subledger, NAV, entity, and period information.

Mitigation: Scope tool and data access to the relevant fund, entity, period, and workflow, and prefer read-only access where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/financial-fund-ops)
- [Referenced financial-services repository in artifact](https://github.com/anthropics/financial-services)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Markdown tables, narrative summaries, JSON objects, and draft journal-entry text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are drafts for review and do not post adjustments or edit source statements.]

## Skill Version(s):

1.0.0 (source: server release evidence, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
