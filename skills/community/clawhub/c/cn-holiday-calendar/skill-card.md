## Description: <br>
Queries gov.cn Chinese holiday notices to determine China workdays, holidays, make-up workdays, and lunar calendar details for a specific date or month. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blueworld415](https://clawhub.ai/user/blueworld415) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to answer China holiday and workday questions for single dates or whole months, including statutory holidays, weekend make-up workdays, lunar dates, and solar terms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A helper can fetch arbitrary web addresses during holiday notice refresh instead of being limited to official gov.cn notice hosts. <br>
Mitigation: Run the skill in a network-restricted environment, prefer cached yearly data, and use a revised version that allowlists HTTPS gov.cn notice hosts while blocking redirects to internal or private addresses. <br>
Risk: Holiday data refresh writes yearly cache files for later answers. <br>
Mitigation: Keep cache writes limited to the documented cache directory and review generated cache JSON before relying on refreshed data. <br>


## Reference(s): <br>
- [Skill instructions](SKILL.md) <br>
- [README](README.md) <br>
- [Gov Holiday Reference](references/api_reference.md) <br>
- [ClawHub release page](https://clawhub.ai/blueworld415/cn-holiday-calendar) <br>
- [gov.cn holiday search endpoint](https://sousuoht.www.gov.cn/athena/forward/2B22E8E39E850E17F95A016A74FCB6B673336FA8B6FEC0E2955907EF9AEE06BE) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Concise structured text or Markdown tables, with optional JSON-like calendar details when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-date answers include workday status, weekday, holiday name when applicable, lunar date, and solar term; month answers use compact date tables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
