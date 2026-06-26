## Description: <br>
Chinese Almanac (Xie Ji Bian Fang Shu) calculates auspicious dates for marriage, business, moving, travel, and other events using traditional Chinese almanac systems such as 12 Day Officers, Yellow/Black Roads, and Pengzu Taboos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ikplpeter](https://clawhub.ai/user/ikplpeter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to select culturally auspicious dates for life events such as marriage, opening a business, moving, signing contracts, travel, worship, seeking wealth, starting a job, and engagement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary notes overly broad activation phrases, especially the Japanese term for clock. <br>
Mitigation: Narrow trigger phrases before deployment so the skill activates only for almanac or date-selection requests. <br>
Risk: Users may treat culturally based date-selection output as professional, legal, financial, medical, or safety advice. <br>
Mitigation: Present results as cultural or entertainment guidance and require independent review for consequential decisions. <br>
Risk: The documentation links to an external demo site that is separate from the local CLI behavior. <br>
Mitigation: Review the external site independently before directing users to it or relying on it in a deployment. <br>
Risk: Release evidence lists license MIT-0, while artifact/package.json lists MIT. <br>
Mitigation: Confirm the authoritative license terms before publication or downstream redistribution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ikplpeter/chinese-almanac) <br>
- [Publisher profile](https://clawhub.ai/user/ikplpeter) <br>
- [Online demo in English](https://halfct.ltd/zeri?lang=en) <br>
- [Online demo in Chinese](https://halfct.ltd/zeri?lang=zh) <br>
- [Online demo in Japanese](https://halfct.ltd/zeri?lang=ja) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON almanac date-selection results with dates, scores, auspicious and inauspicious activities, and related traditional indicators] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports CLI-style month and activity inputs, optional best-date selection, and localized output.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
