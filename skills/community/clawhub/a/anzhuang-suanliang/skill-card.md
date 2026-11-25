## Description:

Produces rough installation quantity estimates and material plan drafts from drawing-reader contracts, without providing pricing or settlement quantities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

CC-BY-NC-SA-4.0

## Use Case:

MEP engineers and quantity surveyors use this skill to turn drawing-reader contracts or scan indexes into draft quantity takeoffs and material plans for budgeting, procurement planning, drawing review, and cross-checking with professional software.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security report rates the release suspicious and cites automatic installation and execution of a separate skill, an environment-selected validator, and behavior that may not match the stated quantity-planning purpose; the scan is partial because a referenced path was missing.

Mitigation: Review the install and execution paths, the environment-selected validator, and the missing referenced path before running; use only trusted dependency locations and check outputs against the drawings and professional software.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lisong2003-lgtm/skills/anzhuang-suanliang)
- [Quantity rules and workflow](references/on-demand.md)
- [Input contract requirements](references/base-contract.md)
- [Loss rules](references/loss_rules.json)
- [Standard rules](references/standard_rules.json)
- [Bus integration guide](docs/bus-integration.md)

## Skill Output:

**Output Type(s):** [Files, JSON, Markdown, Analysis]

**Output Format:** [XLSX workbook, JSON, Markdown, and CSV reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft quantity and material planning outputs; no pricing or settlement quantities. Human review is required for flagged assumptions and drawing ambiguities.]

## Skill Version(s):

0.4.39 (source: frontmatter, CHANGELOG released 2026-11-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
