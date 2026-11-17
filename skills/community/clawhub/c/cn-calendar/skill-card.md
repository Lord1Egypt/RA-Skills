## Description:

Helps agents answer questions about mainland China public holidays, adjusted workdays, workday calculations, and enterprise tax filing calendar dates using bundled 2025-2026 data and referenced government sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linweibin6992-blip](https://clawhub.ai/user/linweibin6992-blip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer user questions about China workdays, public holidays, adjusted workdays, business-day arithmetic, and tax filing deadline calendars. Tax deadline answers should prefer the bundled year-specific filing calendar or official sources over inferred date calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags that the skill can persistently rewrite executable query code when adding newly fetched calendar data.

Mitigation: Require explicit review and approval before remote fetches or persistent updates, and prefer storing newly validated calendar data as data files rather than modifying Python source.

Risk: Tax filing deadline guidance is compliance-sensitive, and the security assessment warns against relying on inferred deadline commands for tax compliance.

Mitigation: Use year-specific official filing calendar references or official tax sources for deadline answers, and avoid using inferred workday-only deadline calculations as authoritative tax advice.

## Reference(s):

- [ClawHub cn-calendar release page](https://clawhub.ai/linweibin6992-blip/skills/cn-calendar)
- [2025 mainland China public holidays and adjusted workdays](references/holidays-2025.md)
- [2026 mainland China public holidays and adjusted workdays](references/holidays-2026.md)
- [China enterprise tax filing calendar](references/tax-filing-calendar.md)
- [2026 enterprise tax filing calendar](references/tax-filing-calendar-2026.md)
- [NateScarlet holiday-cn data index](https://github.com/NateScarlet/holiday-cn)
- [State Taxation Administration of China](https://www.chinatax.gov.cn/)
- [12366 tax calendar endpoint](https://12366.chinatax.gov.cn/bsfw/calendar/getCalendarListForMonth)
- [2026 State Council holiday notice](https://www.gov.cn/zhengce/zhengceku/202511/content_7047091.htm)
- [2025 State Council holiday notice](https://www.gov.cn/zhengce/zhengceku/202411/content_6986383.htm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown and plain text with optional shell commands or JSON-like command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read bundled reference files and propose or run local Python scripts for calendar lookups.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
