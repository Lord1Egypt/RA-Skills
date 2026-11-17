## Description:

Audits a domain's authority, trust, and citation readiness against a declared peer cohort using a 40-item CITE profile with explicit evidence gaps and verified manipulation or penalty veto checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

SEO/GEO practitioners, marketers, and agent operators use this skill to audit one domain's citation-trust profile against a locked market peer cohort and identify evidence gaps, veto risks, and prioritized fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private analytics, console exports, or backlink data may contain sensitive site information.

Mitigation: Provide private data only when it is intended for the audit, and authorize persistence only when a saved audit artifact is desired.

Risk: Missing peer cohort, market, stage, domain type, or private evidence can prevent a complete score and leave the audit undecided.

Mitigation: Declare the target, observation date, market, entity stage, domain type, locked peer cohort, evidence window, and any unavailable qualified items before relying on the result.

Risk: CITE output can be misread as a prediction that answer engines will cite the audited domain.

Mitigation: Use the result as an advisory citation-trust assessment and review evidence gaps, veto checks, and confidence before making publication or campaign decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/aaron-he-zhu/skills/domain-authority-auditor)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Standalone auditor runtime](references/auditor-runtime.md)
- [Example CITE domain authority report](references/example-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown audit report with explicit status, verdict, score_state, score tables, evidence gaps, and optional validated audit artifact.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist a permissioned v3 audit artifact only with explicit user authorization; standalone installs fail closed without scoring when the verified runtime is unavailable.]

## Skill Version(s):

19.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
