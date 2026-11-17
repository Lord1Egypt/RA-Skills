## Description:

基于清乾隆钦定《协纪辨方书》的古典择日系统，融合黄道黑道十二神、建除十二神、天德月德天赦、凶煞、彭祖百忌、奇门遁甲和五行生克，为结婚、开业、搬家、签约、出行等活动提供择吉选日报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ikplpeter](https://clawhub.ai/user/ikplpeter)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate Chinese classical almanac date-selection analysis for supported activities such as weddings, business openings, moving, contracts, travel, worship, and appointments. It can optionally consider user-provided 八字 locally when scoring dates and recommending auspicious hours.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 八字 input can contain personal information even though the inspected code only uses it locally for scoring.

Mitigation: Collect only the 八字 needed for the requested analysis and avoid logging, sharing, or persisting it outside the local run.

Risk: Artifact documentation contains stale script-name examples that differ from the inspected executable.

Mitigation: Run the released CLI through scripts/almanac.js and treat older zeri.js or zhuanshi.js examples as documentation drift.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ikplpeter/skills/classical-almanac)
- [协纪辨方书 · 择日体系参考](references/xieji-bianfang.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese-language console text and Markdown guidance with date scores, auspicious-hour recommendations, 宜忌 details, and almanac factors.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js >=18 and no external dependencies; no network use, file mutation, or persistence was reported by security evidence.]

## Skill Version(s):

1.0.0 (source: server release, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
