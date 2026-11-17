## Description:

Scans blind-bid technical submissions for mechanical formatting compliance and identity leakage in text or document metadata, then produces a requirement-versus-current-state risk report with revision instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External bidders and bid-preparation teams use this skill before sealing or uploading technical blind-bid documents to compare tender formatting requirements against a Word or PDF submission, find bidder-identifying text or metadata, and prepare remediation steps. It supports mechanical compliance review only and does not evaluate technical merit or replace final human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unpinned runtime Python package installation as review-worthy.

Mitigation: Install and run the scanner in a controlled environment with preinstalled, pinned parser packages before handling real bid files.

Risk: Bid documents may be confidential, and scan outputs or logs can contain sensitive excerpts.

Mitigation: Run the skill in a controlled local workspace, avoid shared stdout or log capture, and delete intermediate scan files and reports according to the user's retention policy.

Risk: Generated reports include publisher attribution and a WeChat feedback footer unless the skill is changed.

Mitigation: Review generated reports before circulation and remove or adapt attribution/footer text when it conflicts with organizational procurement or confidentiality rules.

## Reference(s):

- [Blind bid formatting specifications and tolerance baseline](references/blind_bid_specs.md)
- [Identity leakage patterns and safe rewrite guidance](references/identity_patterns.md)
- [Blind bid failure and point-loss cases](references/blind_bid_failure_cases.md)
- [Printable blind bid self-check list](references/self_check_list.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report with comparison tables, risk labels, remediation instructions, and inline command or code blocks; scanner scripts produce JSON for the agent to analyze.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include red/yellow risk labels, manual-review notes for unreliable PDF or image fields, and optional VBA/Python cleanup snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
