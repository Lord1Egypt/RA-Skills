## Description:

Chinese Almanac helps agents run a local date-selection CLI that rates auspicious dates for life events using traditional Chinese almanac systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ikplpeter](https://clawhub.ai/user/ikplpeter)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to evaluate dates for events such as marriage, business opening, moving, contracts, travel, renovation, worship, wealth-seeking, starting a job, or engagement. Results should be treated as traditional or entertainment-oriented guidance rather than authoritative advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat auspicious-date ratings as authoritative planning, financial, legal, medical, or professional advice.

Mitigation: Present results as traditional or entertainment-oriented guidance and require users to apply independent judgment for consequential decisions.

Risk: The documentation appears broader than the actual scoring logic.

Mitigation: Validate important outputs against the implemented CLI behavior and avoid promising unsupported almanac factors.

Risk: Broad trigger terms may activate the skill when a user only wants general calendar information.

Mitigation: Confirm the user wants Chinese almanac date-selection guidance before running or applying the CLI.

## Reference(s):

- [Chinese Almanac on ClawHub](https://clawhub.ai/ikplpeter/skills/chinese-almanac)
- [Online demo - English](https://halfct.ltd/zeri?lang=en)
- [Online demo - Chinese](https://halfct.ltd/zeri?lang=zh)
- [Online demo - Japanese](https://halfct.ltd/zeri?lang=ja)
- [Online demo - Vietnamese](https://halfct.ltd/zeri?lang=vi)
- [Online demo - Thai](https://halfct.ltd/zeri?lang=th)
- [Online demo - Malay](https://halfct.ltd/zeri?lang=ms)
- [Online demo - Hindi](https://halfct.ltd/zeri?lang=hi)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with optional CLI commands and JSON output from the local almanac script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports English, Chinese, and Japanese CLI labels; artifact documentation also links demos for Vietnamese, Thai, Malay, and Hindi.]

## Skill Version(s):

2.0.0 (source: server release evidence and SKILL.md frontmatter; artifact/package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
