## Description:

Advises on career decisions including offer evaluation, salary and equity negotiation, promotions, pivots, and layoff response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and career changers use this skill to evaluate offers, negotiate compensation, compare equity packages, pursue promotions, decide whether to stay or leave, and respond to layoffs, PIPs, firings, or rescinded offers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain sensitive compensation, visa, family, offer, and career preference details in local plaintext files under ~/Clawic/data/career/.

Mitigation: Install only if local career-record persistence is acceptable; periodically review or delete the directory and avoid sharing details that should not be retained.

## Reference(s):

- [ClawHub Career Skill Page](https://clawhub.ai/ivangdavila/skills/career)
- [Clawic Career Skill Page](https://clawic.com/skills/career)
- [Career Skill Definition](artifact/SKILL.md)
- [Setup and Local Memory Behavior](artifact/setup.md)
- [Career Memory Template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with structured checklists, negotiation scripts, and optional local memory updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist user career facts, preferences, and observed patterns under ~/Clawic/data/career/ when the user reveals relevant information.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
