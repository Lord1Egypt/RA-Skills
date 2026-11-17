## Description:

保证金收退台账逐项核对，执行逐行复算、合计勾稽、重复与空缺检测，并为每条结论引用原文依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and cashiering staff use this skill during monthly close, reconciliation, and inventory checks to validate Chinese bid deposit refund ledgers. It checks row arithmetic, total reconciliation, duplicate bidder/project rows, blank or placeholder required fields, and cites source rows for findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free release omits several checks that users may expect from a complete bid deposit review, including date inversion, overdue refund timing, abnormal guarantee ratio, and negative or excessive refund checks.

Mitigation: Show the checks performed and checks not run in the output, and require users to review omitted checks before relying on the result.

Risk: The skill reads user-selected ledger material from local files, which may contain sensitive commercial or finance data.

Mitigation: Run it only in a trusted local environment and provide only the ledger text required for the check.

Risk: Material that is missing, malformed, or lacks recognizable headers can lead to no executable check rather than a business conclusion.

Mitigation: Treat insufficient-input responses as a request for more material, not as a clean result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/bid-deposit-refund-check-free)
- [Skill documentation](artifact/SKILL.md)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Human-readable text or JSON containing deterministic ledger findings with cited source rows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; reads a user-supplied ledger text or JSON file and does not use network access.]

## Skill Version(s):

1.0.56 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
