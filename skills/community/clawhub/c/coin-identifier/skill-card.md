## Description:

Identify coins from photos using evidence-based visual checks, ranked candidates, mint-mark reasoning, and a reusable local catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to identify coins from user-provided photos, compare ranked candidates, request missing visual evidence, and optionally keep approved local identification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local coin-identification notes could accidentally include unrelated personal information.

Mitigation: Ask for user approval before local storage and save only durable coin-identification preferences or approved identification notes.

Risk: Photo-only identification can be mistaken for grading, authenticity, composition, or market-value advice.

Mitigation: Return ranked candidates with confidence and explicitly state that photos do not prove authenticity, grade, metal purity, or value.

Risk: Poor image quality can lead to overconfident or incorrect identification.

Mitigation: Check glare, blur, crop, orientation, and missing obverse, reverse, or edge views, then ask for the single most useful next image or measurement.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/coin-identifier)
- [Skill Homepage](https://clawic.com/skills/coin-identifier)
- [Coin Evidence Guide](artifact/evidence-guide.md)
- [Setup Guide](artifact/setup.md)
- [Memory Template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown responses with ranked candidate lists, confidence bands, missing-evidence notes, and optional local note templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local memory and identification notes only after user approval; no network requests are described.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
