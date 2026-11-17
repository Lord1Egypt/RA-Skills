## Description:

Generate repeatable, audit-friendly browser-agent workflow templates for form filling, case routing, portal operations, research capture, and approval-gated web actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to generate reusable browser-agent workflow templates for form filling, case routing, portal operations, research capture, and approval-gated web actions before connecting to live browser or computer-use tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user-selected steps file may contain sensitive or inappropriate local content.

Mitigation: Avoid passing sensitive files as --steps and review custom workflow steps before using the generated template.

Risk: A user-selected output path may create or overwrite a file.

Mitigation: Choose an output path that is safe for the skill to create or replace.

Risk: Generated browser-action templates could be misapplied to live systems without sufficient review.

Mitigation: Review approval gates, evidence capture requirements, and rollback notes before connecting the template to live browser or computer-use tools.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, JSON, Configuration, Guidance]

**Output Format:** [Markdown document or JSON object containing workflow steps, approval gates, evidence requirements, error handling, and a handoff schema.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write generated output to a user-selected path; optional workflow steps are read from a JSON file.]

## Skill Version(s):

1.0.0 (source: server release metadata, changelog: Initial release 2026-04-30)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
