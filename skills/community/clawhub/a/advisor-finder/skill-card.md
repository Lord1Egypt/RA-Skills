## Description:

Find and analyze potential academic advisors, supervisors, or faculty for a target university, school, department, or research direction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntsl-ye](https://clawhub.ai/user/ntsl-ye)

### License/Terms of Use:

MIT-0

## Use Case:

Students, applicants, and academic researchers use this skill to find and rank potential advisors for a target university, department, or research direction. It emphasizes official pages, recent publication evidence, fit assessment, and explicit uncertainty when recommending whom to contact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advisor recommendations can be misleading if school websites are incomplete, blocked, stale, or inconsistent.

Mitigation: Prefer official university, department, lab, and faculty pages; downgrade evidence quality and state uncertainty when the verification chain is weak.

Risk: The skill may overstate a faculty member's current research direction or recruiting status from sparse public evidence.

Mitigation: Require repeated recent evidence for strong recommendations and avoid claiming that a faculty member is recruiting unless public evidence supports it.

Risk: The artifact instructs direct Chinese output, which may not match every user's preferred language.

Mitigation: Install or use the skill when Chinese-language advisor shortlists are acceptable, or adjust the output-language instruction to follow the user's preference.

## Reference(s):

- [Advisor Finder skill page](https://clawhub.ai/ntsl-ye/skills/advisor-finder)
- [China Top University School Hints](references/china-top-university-hints.md)
- [GitHub Datasets and Repositories Useful for Advisor Finder](references/github-datasets.md)
- [Advisor Finder Output Template](references/output-template.md)
- [Research Keyword Hints](references/research-keywords.md)
- [Scoring Template](references/scoring-template.md)
- [Site Failure Playbook](references/site-failure-playbook.md)
- [Top University Site Hints](references/top-university-sites.md)
- [CSrankings](https://csrankings.org)
- [CSrankings repository](https://github.com/emeryberger/CSrankings)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown shortlist with ranked faculty profiles, evidence notes, fit assessment, risks, and next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Direct Chinese prose; uses Priority A/B/C ranking bands and High/Medium/Low evidence labels.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
