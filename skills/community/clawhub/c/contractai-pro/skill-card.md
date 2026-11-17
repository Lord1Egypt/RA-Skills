## Description:

ContractAI Pro helps agents run a local Chinese-language contract review and template generation workflow using rule-based checks and built-in contract templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiyee1688](https://clawhub.ai/user/qiyee1688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, legal operations teams, and business users can use this skill to screen Chinese-language contract text for common rule-based risk patterns and generate starter contract templates for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marketing text claims AI legal analysis, current law coverage, OCR/PDF support, and lawyer-grade review beyond the local rule-based behavior identified in security evidence.

Mitigation: Treat outputs as heuristic screening and template drafting aids, then have qualified legal counsel review important contracts before signing.

Risk: Contracts may contain confidential information, and the scripts read local contract files and can write explicit report or contract output files.

Mitigation: Use only in workflows where local processing and saved report files are acceptable, and avoid entering confidential contracts without appropriate handling controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiyee1688/skills/contractai-pro)
- [Publisher profile](https://clawhub.ai/user/qiyee1688)
- [README](README.md)
- [Example review report](examples/review_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown reports, generated contract Markdown files, command-line text, and Python command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local file inputs and optional exported report paths; security evidence identifies no hidden network, persistence, credential access, or unsafe execution behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
