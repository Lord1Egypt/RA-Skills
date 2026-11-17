## Description:

Turn user-supplied fund factsheet points into one still per page. This fund factsheet page studio lays out each prospectus page still from the supplied fund factsheet. Use it for factsheet page graphics, fund page set layouts, and page-by-page fund stills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn approved fund factsheet page points into page-by-page prospectus stills. It plans one still per named page, confirms billable generation, submits Beatra image tasks, and reports returned artifacts and charges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package requests broad shared Beatra account authorization, including billable and state-changing capabilities beyond factsheet image generation.

Mitigation: Install only when that scope is acceptable, keep the credential private, and revoke the device authorization from the Beatra Console when the skill is no longer trusted or needed.

Risk: Billable image generation can charge credits, and retries can duplicate work if request identity changes.

Mitigation: Confirm the production card before paid calls, use one opaque client request ID per page, and retry only unchanged payloads with the same identity after transport uncertainty.

Risk: Silent automatic updates can change package code after installation.

Mitigation: Use the documented update controls to disable automatic checks when review-before-update is required.

Risk: Uploaded reference files become available to Beatra.

Mitigation: Upload only reference files the user intends to share, and treat scans or photos as visual references rather than sources for missing facts.

Risk: Generated small type or financial factsheet text may be unreadable or misleading if treated as certified disclosure.

Mitigation: Review visible printed text against the confirmed page list and report unread small type as a review item, not a certified disclosure or performance forecast.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/beatra-ai/skills/fund-page-set)
- [Fund-page workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [MCP connection](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and returned image artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a free page plan before billable image generation; final delivery includes page order, task IDs, dimensions, formats, resolved models, and net charged credits.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
