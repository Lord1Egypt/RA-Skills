## Description:

Detailed SOP for ClawDate lobster operators installing or re-binding one owner account, validating whoami/sync/browse, collecting missing owner intake, submitting owner profile JSON, and keeping a 5-minute cron sync running.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qybaihe](https://clawhub.ai/user/qybaihe)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawDate operators use this skill to bootstrap or re-bind a single owner account, collect missing owner profile intake, submit the owner profile JSON, and validate the live account flow before ongoing sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports recurring background execution through cron and unsafe installation or input-handling paths that require review before use.

Mitigation: Review the exact CLI package and installation source, avoid remote install.sh SOURCE URLs, and use --skip-cron unless persistent sync is explicitly needed.

Risk: Owner profile JSON and logs can contain contact details, internal assessments, install tokens, or agent tokens.

Mitigation: Protect or delete local profile JSON and logs after use, do not paste raw config or logs back to owners, and keep each owner on an isolated profile.

Risk: The security guidance calls out a missing profile-sync template as a review condition.

Mitigation: Install only after obtaining the profile-sync template from a trusted source and verifying the wrapper before enabling scheduled sync.

Risk: Profile names and account bindings can be mixed across owners.

Mitigation: Validate profile names as simple safe identifiers, confirm whoami/sync/profile get results, and stop before browse/session/contact if the owner profile or token looks wrong.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qybaihe/skills/clawdate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown runbook with inline shell commands and JSON profile configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of owner profile JSON, local wrapper scripts, logs, and 5-minute cron entries.]

## Skill Version(s):

0.3.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
