## Description: <br>
Daily Xuanzang helps an agent deliver progressive bilingual readings of the Great Tang Records on the Western Regions, with source excerpts, translation, commentary, route maps, and optional narration or scene art. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yumyumtum](https://clawhub.ai/user/yumyumtum) <br>

### License/Terms of Use: <br>
GPL-3.0-or-later <br>


## Use Case: <br>
External users and agents use this skill to produce a daily illustrated pilgrimage-style reading experience for Xuanzang's Western Journey. It supports sequential lectures with classical Chinese excerpts, vernacular Chinese or English translation, contextual explanation, and route-map guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves and advances local reading progress after an episode is delivered. <br>
Mitigation: Review progress behavior before installation, and advance the cursor only after the expected lecture and configured media outputs are complete. <br>
Risk: Optional scheduling, image, voice, or Telegram delivery setup can publish or generate content beyond the immediate text lecture. <br>
Mitigation: Use explicit trigger phrases and review any scheduling, media-generation, or delivery configuration before enabling it. <br>


## Reference(s): <br>
- [Daily Xuanzang ClawHub release page](https://clawhub.ai/yumyumtum/daily-xuanzang) <br>
- [Structure Reference](references/structure.md) <br>
- [Lecture Style Guide](references/style-guide.md) <br>
- [Bundled CBETA T51n2087 source volumes](data/volumes/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown lecture content with route-map guidance, optional media-generation guidance, and inline shell commands for progress management] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save local reading progress and may produce optional map, image, or voice artifacts when configured.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
