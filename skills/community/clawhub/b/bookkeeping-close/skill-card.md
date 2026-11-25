## Description:

Helps small and midsize businesses reconcile bank and card activity, categorize transactions, review month-end close steps, and prepare a close package for an accountant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bankgpt](https://clawhub.ai/user/bankgpt)

### License/Terms of Use:

MIT-0

## Use Case:

Small-business owners and bookkeepers use the skill to compare bank or card statements with ledger records, organize transactions and review items, and prepare a month-end close package for an accountant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes broad activation on “reconcile” and unclear tool scope.

Mitigation: Review the activation conditions and inspect available connector tools and permissions before enabling the skill.

Risk: Security analysis was partial because a referenced local path was missing, so the evidence is incomplete.

Mitigation: Resolve the missing path and complete review of all listed components before deployment.

Risk: Matching or categorization may leave unexplained, uncertain, or tax-sensitive items.

Mitigation: Keep unexplained variances visible, review uncertain categorization, and route tax-sensitive questions and proposed adjustments to the accountant.

## Reference(s):

- [Platform Notes: QuickBooks Online, Xero, Bank Files, Mercury](references/platform-notes.md)
- [Categorization Rules](references/categorization-rules.md)
- [Month-End Close Checklist](references/close-checklist.md)
- [Worked Example](examples/worked-example.md)
- [BankGPT.IO](https://bankgpt.io/)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV, JSON, Bookkeeping guidance]

**Output Format:** [Markdown close package with optional CSV match and exception files and a JSON summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proposed adjusting entries are for accountant review; connector write actions require explicit approval.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
