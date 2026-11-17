## Description:

Audit and remove unused, test, or deprecated forms from HubSpot. Identifies forms with zero submissions, forms not embedded on any page, and test forms left over from development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomgranot](https://clawhub.ai/user/tomgranot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to audit HubSpot forms, identify stale or test forms, and carry out a documented cleanup with manual checks before deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent could recommend deleting a HubSpot form that is still used by a live page, workflow, pop-up, or slide-in CTA.

Mitigation: Review each deletion candidate manually against active pages, workflow enrollment triggers, and CTA usage before removal.

Risk: Deleted HubSpot form definitions cannot be restored.

Mitigation: Export form definitions before deleting any form with submissions and keep a cleanup log of every removed form.

Risk: A broad HubSpot API token could expose more access than the cleanup task requires.

Mitigation: Use the least-privileged HubSpot token available for form auditing and deletion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomgranot/skills/cleanup-forms)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with checklist-style instructions and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes manual review checkpoints before deletion.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
