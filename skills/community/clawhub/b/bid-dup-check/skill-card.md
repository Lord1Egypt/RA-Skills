## Description:

Bid Dup Check helps agents screen Chinese bid and tender documents for duplicate text, key information collisions, document metadata similarities, table similarities, and two-document diffs, then produce structured risk reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement teams, bidders, and reviewing agents use this skill to triage 2-10 Chinese bid or tender files for similarity and possible collusion risk before human review. It supports preliminary screening and report generation, not formal committee decisions or legal determinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive procurement and bid documents and may leave extracted JSON or images in the workspace.

Mitigation: Use a locked runtime, restrict access to uploaded and extracted files, and remove temporary extraction artifacts after the report is delivered.

Risk: Generated similarity or collusion findings are preliminary and may be incorrect or incomplete.

Mitigation: Require human review before procurement, compliance, legal, or committee decisions, and treat high-risk findings as leads for verification.

Risk: User-facing reports include a mandatory third-party attribution and contact footer.

Mitigation: Review whether the footer is acceptable for formal procurement or compliance reporting before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chesaram/skills/bid-dup-check)
- [Publisher Profile](https://clawhub.ai/user/chesaram)
- [README](artifact/README.md)
- [Detection Rules Reference](artifact/references/detection_rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Structured JSON findings, Markdown report text, DOCX report file, and concise conversational summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports .docx, text-layer .pdf, and .txt inputs; focuses on Chinese bid documents; extracted JSON and images may remain in the workspace until cleanup.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
