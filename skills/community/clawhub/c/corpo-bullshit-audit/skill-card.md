## Description:

Audit corporate text for jargon/evasion and compute bullshit-to-content ratio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, communications reviewers, and managers use this skill to audit emails, memos, job ads, performance reviews, press releases, transcripts, and other corporate copy for vague or evasive language and to rewrite it in plainer terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Corporate writing submitted for audit may contain sensitive workplace information.

Mitigation: Use the skill only in environments where the submitted text is appropriate to share and review.

Risk: The audit may overstate a phrase's significance when a term is used precisely in context.

Mitigation: Apply the skill's calibration guidance: flag phrases only when they hide responsibility, avoid specifics, inflate routine work, mask bad news, or replace concrete action with theater.

## Reference(s):

- [Corporate Bullshit Phrase Reference](references/corpo-bullshit-phrases.md)
- [The MBA Jargon Exhaustive List](https://bullshitgenerator.blogspot.com/2010/01/mba-jargon-exhaustive-list.html)
- [58 awful corporate jargon phrases you can't escape](https://www.techtarget.com/whatis/feature/Awful-corporate-jargon-phrases-you-cant-escape)
- [Decoding Corporate BS: 27 Phrases That Expose Bad Managers](https://read.thegoodboss.com/p/decoding-corporate-bullsht-27-phrases)
- [Corporate Bullshit Dictionary](https://bsdict.com/dictionary)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit with verdict, ratio, findings, phrase hits, rewrite, and clarification questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a bullshit-to-content ratio, severity ratings, and plain-language rewrites when the requested audit calls for them.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
