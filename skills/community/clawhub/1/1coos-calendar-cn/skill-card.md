## Description: <br>
Queries Chinese traditional calendar and almanac information, including lunar dates, huangli, solar terms, five elements, auspicious and inauspicious activities, ganzhi, Buddhist calendar details, and Taoist calendar details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1coos](https://clawhub.ai/user/1coos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up Chinese calendar, lunar date, and huangli details for a requested Gregorian or lunar date. It is intended for informational calendar lookup and configurable almanac output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be invoked for a broad range of Chinese calendar-related questions. <br>
Mitigation: Review agent routing and invocation behavior so it is used only for intended Chinese calendar and almanac lookups. <br>
Risk: A user-supplied --config path could point to sensitive local files. <br>
Mitigation: Use only non-sensitive configuration files when passing --config. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1coos/1coos-calendar-cn) <br>
- [Module Configuration Reference](references/modules.md) <br>
- [lunar-typescript](https://github.com/6tail/lunar-typescript) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style text with calendar sections and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Bun and accepts optional date, lunar-date, help, and config-file parameters.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
