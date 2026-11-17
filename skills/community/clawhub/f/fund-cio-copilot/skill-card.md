## Description:

产业基金 CIO Copilot supports industrial fund GPs, investment directors, and investment committees across BP screening, evaluation analysis, IC preparation, portfolio follow-up, and weekly industry radar workflows while keeping final investment decisions with humans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

External fund teams, investment managers, IC members, and local industrial investment stakeholders use this skill to structure project screening, due diligence analysis, IC recommendations, portfolio monitoring, and public-market intelligence into traceable decision-support artifacts. It is explicitly positioned as analysis support, not an autonomous investment decision-maker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store sensitive fund records and decision history in local JSONL and Markdown memory files.

Mitigation: Use the skill in an isolated workspace with appropriate file permissions and treat generated memory files as confidential records.

Risk: The skill can create external Tencent Docs documents or run scheduled publication-style workflows.

Mitigation: Require human approval before Tencent Docs publication or scheduled automation, especially for IC materials, portfolio records, or fund-specific analysis.

Risk: Raw web, project, or company text may be promoted into memory or analysis outputs without enough review.

Mitigation: Sanitize raw inputs, label verification status, and avoid writing unreviewed source text into Decision Memory.

Risk: Investment analysis outputs could be mistaken for final investment decisions.

Mitigation: Keep the documented human-in-the-loop boundary: all recommendations remain analysis support and final decisions require IC or authorized human review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/perrykono-debug/skills/fund-cio-copilot)
- [Publisher Profile](https://clawhub.ai/user/perrykono-debug)
- [Skill Definition](artifact/SKILL.md)
- [Decision Object Schema](artifact/decision-object.md)
- [Decision Memory](artifact/decision-memory.md)
- [Investment Mandate](artifact/mandate.md)
- [Weekly Radar Mode](artifact/mode-weekly-radar.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, guidance]

**Output Format:** [Markdown reports, structured JSON decision objects, JSONL memory records, and configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include mandatory investment-decision disclaimers, human-readable artifacts separated from machine-readable decision objects, and persistent local memory/configuration files when workflows require them.]

## Skill Version(s):

2.6.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
