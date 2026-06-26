## Description: <br>
Daily horoscope for all 12 zodiac signs -- love, career and finance scores, lucky color, number and direction, daily affirmation, morning and evening push, and bilingual EN/CN output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to generate daily Western astrology readings for all 12 zodiac signs, including love, career and finance scores, lucky elements, and affirmations in English and Chinese. It can also configure optional morning and evening scheduled push messages through supported channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional scheduled push messages may continue after a user no longer wants daily horoscope notifications. <br>
Mitigation: Review push settings before enabling them and use the documented off command to disable scheduled messages. <br>
Risk: Broad astrology trigger phrases may activate the skill when a user intended a different astrology-related workflow. <br>
Mitigation: Narrow activation phrases in the host agent when generic astrology terms trigger the skill too often. <br>


## Reference(s): <br>
- [ClawHub Daily Astro skill page](https://clawhub.ai/jiajiaoy/daily-astro) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Plain text or Markdown horoscope prompts and scheduled-push configuration commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual EN/CN content; optional push schedules support telegram, feishu, slack, and discord channels.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
