## Description:

Automates AudTools batch collection by reading Shopify category URLs from a CSV, filling the AudTools collection form with each URL, setting product count to 9999, and submitting entries at two-second intervals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qirongzhang](https://clawhub.ai/user/qirongzhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate bulk submission of Shopify category URLs into AudTools for product collection workflows. It is intended for CSV-driven collection batches where the operator can review inputs and recover unintended submissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk CSV inputs may cause many URLs to be submitted through a logged-in AudTools browser.

Mitigation: Review the CSV before running and prefer a dry-run or explicit confirmation step for batches.

Risk: Loose page and form matching may submit to an unintended field or page state.

Mitigation: Use exact form selectors and verify the AudTools origin before each submission.

Risk: Dependency sources deserve review before execution.

Mitigation: Regenerate dependencies from a trusted registry and review the resolved lockfile before running.

Risk: Unintended AudTools submissions may affect the operator account.

Mitigation: Use an account where unintended submissions are recoverable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qirongzhang/skills/audtools-shopify-collector)
- [AudTools Collection Page](https://www.audtools.com/users/shopns#/users/shopns/collecs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May launch a visible browser session and submit CSV-provided URLs through a logged-in AudTools account.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
