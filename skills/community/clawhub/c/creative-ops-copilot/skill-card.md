## Description:

Turn messy client briefs into a production-ready plan for motion design/VFX projects: scope, assumptions/exclusions, deliverables matrix, schedule/milestones, review rounds, and estimate/quote.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiseape11](https://clawhub.ai/user/wiseape11)

### License/Terms of Use:


## Use Case:

Creative operations users and motion design or VFX producers use this skill to convert client briefs, emails, or chat notes into client-ready production plans, estimates, invoice drafts, and optional project folder skeletons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional invoice push can send client and project invoice data to the configured invoicing endpoint.

Mitigation: Use --push-invoice only after reviewing references/config.json, especially invoicingApi.baseUrl and apiKey.

Risk: The skill writes production planning files and invoice drafts into the selected output directory.

Mitigation: Run it in the intended project workspace and review generated plan, estimate, and invoice files before sharing or importing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wiseape11/skills/creative-ops-copilot)
- [config.example.json](references/config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown, JSON, CSV-compatible structured data, shell commands, and project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Always produces docs/creative-ops/plan.md, docs/creative-ops/estimate.json, and docs/creative-ops/invoice-draft.json; can optionally create a project folder skeleton and push an invoice draft to a configured invoicing API.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
