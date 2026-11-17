## Description:

Use this skill when an ERISA plan sponsor, retirement committee member, plan administrator, or benefits counsel needs to draft a fiduciary prudent-process review memo for a 401(k), 403(b), defined-benefit, or health-and-welfare plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

ERISA plan sponsors, retirement committee members, plan administrators, and benefits counsel use this skill to draft a review-ready fiduciary prudent-process memo documenting investment monitoring, fee reasonableness, service-provider review, compliance flags, cybersecurity review, and committee action items.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: A generated fiduciary memo could be treated as legal advice or adopted before qualified review.

Mitigation: Use the output only as a draft and have qualified ERISA counsel review it before committee adoption, execution, or filing use.

Risk: Plan or participant personal data could be included unnecessarily in prompts or memo output.

Mitigation: Avoid providing participant SSNs, account numbers, birth dates, medical data, or unnecessary personal information, and remove any such data before use.

Risk: Critical compliance, fee, fiduciary, or cybersecurity findings may require legal judgment or authorized corrective action.

Mitigation: Route critical deficiencies and compliance failures to ERISA counsel and do not use the skill to file, transmit, or submit documents on behalf of the plan.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/erisa-plan-fiduciary-review-memo)
- [README](artifact/README.md)
- [CHANGELOG](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance]

**Output Format:** [Single markdown draft memo with tables, drafting notes, open action items, and an unsigned attorney review block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafting aid only; generated memo requires review by qualified ERISA counsel before adoption or filing use.]

## Skill Version(s):

0.1.0 (source: server release evidence and CHANGELOG, released 2026-05-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
