## Description:

Turn user-supplied on-site inspection check item names and check points into a four-to-eight still field check set.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Field teams, operations staff, and designers use this skill to turn approved inspection item names and check points into a consistent set of on-site field check stills. It helps plan, confirm, generate, review, and recover billable Beatra image-generation tasks without adding unsupplied inspection conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package uses a shared Beatra device credential with broad media, wallet, task, artifact, voice, and generation authority.

Mitigation: Install only when that account authority is acceptable, keep the device token private, and reconnect or revoke access through the documented Beatra authorization and uninstall flows.

Risk: Local executable package files can silently self-update by default.

Mitigation: Disable automatic updates for this installation with `python3 scripts/mcp_client.py update --auto off` when change control is required.

Risk: Image generation and edits are billable Beatra work.

Mitigation: Require the production confirmation card before paid calls, use one opaque request identity per still, and report only returned `billing.net_charged_credits` as the settled charge.

Risk: Uploaded reference files become available to Beatra for the requested media workflow.

Mitigation: Avoid uploading sensitive local files and treat uploads as optional visual references rather than sources for missing check points.

Risk: Generated stills could be mistaken for official inspection findings or compliance determinations.

Mitigation: Use only user-approved check item names and check points, omit pass/fail results or official stamps unless supplied, and review visible printed text before delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/field-check-set)
- [Beatra skill homepage](https://beatra.ai/skills/field-check-set)
- [Field check pack workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a free pack list before paid image-generation calls; completed work includes generated still artifacts, task IDs, resolved models, dimensions, formats, and net charged credits.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
