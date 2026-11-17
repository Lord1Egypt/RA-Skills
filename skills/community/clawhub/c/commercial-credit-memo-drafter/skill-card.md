## Description:

Commercial Credit Memo Drafter helps commercial loan officers, credit analysts, and relationship managers turn borrower financials and a loan request into a draft Credit Analysis Memorandum with 5Cs analysis, DSCR, leverage, LTV, risk-rating recommendation, covenant package, and recommendation options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Commercial loan officers, credit analysts, relationship managers, and underwriters use this skill to collect borrower and loan facts, draft a 5Cs Credit Analysis Memorandum, compute underwriting ratios, propose covenants, and flag policy exceptions for qualified credit-officer review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Borrower, guarantor, credit bureau, KYC, OFAC, BSA/AML, and beneficial-ownership data may be confidential or regulated.

Mitigation: Use only in an authorized agent environment and summarize sensitive supplied data instead of reproducing it verbatim.

Risk: Drafted credit recommendations or risk ratings could be mistaken for final credit decisions.

Mitigation: Keep the DRAFT - CREDIT OFFICER MUST REVIEW label and route final credit, KYC, OFAC, BSA/AML, and policy decisions to qualified human reviewers.

Risk: Missing or unsupported financial inputs can lead to unreliable ratios, covenants, or policy-exception analysis.

Mitigation: Require source tags and historical or projected period labels for figures, mark unavailable inputs as unknown, and review ratio calculations before relying on the memo.

## Reference(s):

- [Commercial Credit Memo Drafter README](artifact/README.md)
- [Commercial Credit Memo Drafter Skill](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/commercial-credit-memo-drafter)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance]

**Output Format:** [Markdown draft memo with tables, inline source tags, assumptions, open questions, ratio analysis, covenant proposals, and review notices]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are drafts for human review and should retain the DRAFT - CREDIT OFFICER MUST REVIEW notice.]

## Skill Version(s):

0.1.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
