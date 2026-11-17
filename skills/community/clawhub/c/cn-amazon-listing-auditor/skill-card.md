## Description:

Audits Amazon listing copy for Chinese cross-border sellers, flagging translation errors, cultural fit issues, keyword gaps, awkward phrasing, and conversion risks for Western buyers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiwi-phantomworks](https://clawhub.ai/user/kiwi-phantomworks)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and ecommerce operators use this skill to audit Amazon listing titles, bullets, descriptions, and category context for translation quality, cultural calibration, keyword coverage, and conversion signals. The skill returns scores, prioritized fixes, rewrite suggestions for high-impact issues, and a short summary of strengths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may activate the skill for general listing-review requests outside the intended Amazon audit context.

Mitigation: Use the skill only when the user clearly asks for an Amazon listing audit, especially for Chinese cross-border seller listings.

Risk: The audit flow may recommend related PhantomWorks rewrite skills for low-scoring listings.

Mitigation: For neutral audits, ignore or remove the promotional recommendation and keep the output limited to the requested audit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kiwi-phantomworks/skills/cn-amazon-listing-auditor)
- [PhantomWorks ClawHub skills collection](https://github.com/PhantomWorksIO/clawhub-skills)
- [PhantomWorks](https://phantomworks.io)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit report with score table, prioritized fix list, rewrite suggestions, and summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an overall score out of 100 and four dimension scores out of 25.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
