## Description: <br>
Commercial Credit Memo Drafter helps commercial loan officers, credit analysts, and relationship managers turn borrower financials and loan requests into draft Credit Analysis Memoranda with 5Cs analysis, ratios, risk-rating recommendations, covenant packages, and credit-officer review controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Commercial loan officers, credit analysts, underwriters, and relationship managers use this skill to collect borrower and loan-request facts, compute underwriting ratios, and draft a structured Credit Analysis Memorandum for qualified credit-officer review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles confidential borrower, guarantor, financial, credit-policy, bureau, KYC, OFAC, BSA/AML, and beneficial-ownership information in the agent session. <br>
Mitigation: Install and use it only in agent environments approved for that information, and avoid sharing raw confidential data beyond the intended session. <br>
Risk: A generated memo, risk rating, covenant package, or approve/decline recommendation could be mistaken for a binding credit decision. <br>
Mitigation: Treat every output as a draft analytical memo and require qualified credit-officer review before any credit, legal, compliance, or customer-facing action. <br>
Risk: Incomplete or unsourced borrower data can lead to misleading ratios, projections, policy exceptions, or recommendation language. <br>
Mitigation: Require source tags, historical/projected labels, open-question tracking, and verification of assumptions against institution policy and supplied documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/commercial-credit-memo-drafter) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, analysis, guidance] <br>
**Output Format:** [Markdown draft credit memo with tables, source tags, ratio calculations, exception flags, covenant proposals, and open questions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are drafts for human credit-officer review and may include sensitive borrower, guarantor, financial, and credit-policy information supplied by the user.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence; artifact changelog top entry is 0.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
