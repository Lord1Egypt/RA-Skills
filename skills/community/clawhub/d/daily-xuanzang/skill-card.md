## Description:

Guides an agent through daily, bilingual readings of the Great Tang Records on the Western Regions, with progress tracking, route maps, and optional narration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yumyumtum](https://clawhub.ai/user/yumyumtum)

### License/Terms of Use:

GPL-3.0-or-later

## Use Case:

External readers and learners use the skill to read the Great Tang Records on the Western Regions a segment at a time, with Chinese or English translation and historical context. It can also produce route maps and optional narration for each reading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Narration may be sent to an external speech service, which could expose private material.

Mitigation: Review the service's data handling and omit private material unless that sharing is acceptable.

Risk: The suggested TTS package is unpinned, and the security scan was partial.

Mitigation: Assess whether the dependency and tool scope are acceptable, and treat the scan as incomplete evidence.

## Reference(s):

- [ClawHub release](https://clawhub.ai/yumyumtum/skills/daily-xuanzang)
- [Journey structure reference](artifact/references/structure.md)
- [Reading style guide](artifact/references/style-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Images, Audio]

**Output Format:** [A structured Markdown lecture, a bilingual route map image, and optional narrated audio]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One reading segment per episode; route maps are the default, while scene art and narration are optional.]

## Skill Version(s):

0.2.1 (source: package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
