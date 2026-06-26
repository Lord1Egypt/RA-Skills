## Description: <br>
Fortune Daily generates personalized daily, weekly, monthly, or date-specific horoscope readings by combining Western zodiac signs and Chinese zodiac attributes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vccv2rndrv-cyber](https://clawhub.ai/user/vccv2rndrv-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and assistant operators use this skill to generate personalized Chinese-language horoscope readings and optional scheduled daily push messages based on birthday, zodiac sign, Chinese zodiac animal, and preferred detail level. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores birthday, zodiac, Chinese zodiac, and push preference data in MEMORY.md for personalization. <br>
Mitigation: Confirm the user is comfortable with that stored profile data, clear bundled sample data before real use, and provide a way to delete or reset stored profile data. <br>
Risk: Daily push delivery may send personal horoscope content through the configured OpenClaw channel. <br>
Mitigation: Enable scheduled push only after explicit opt-in and verify how the runtime handles message delivery and stored preferences. <br>


## Reference(s): <br>
- [Fortune Daily on ClawHub](https://clawhub.ai/vccv2rndrv-cyber/fortune-daily) <br>
- [Publisher profile: vccv2rndrv-cyber](https://clawhub.ai/user/vccv2rndrv-cyber) <br>
- [Zodiac index reference](references/zodiac-index.md) <br>
- [Zodiac sign reference files](references/signs/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown horoscope readings with optional scheduling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include five reading dimensions, lucky guidance, a daily tip, and push-ready message content.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter and package.json report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
