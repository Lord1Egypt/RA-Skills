## Description: <br>
cn-calendar helps agents query mainland China statutory holidays, workdays, adjusted workdays, and business tax filing calendars, with local 2025-2026 data and public-source fetching for unsupported years. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linweibin6992-blip](https://clawhub.ai/user/linweibin6992-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operations teams, and assistants use this skill to answer mainland China workday and holiday questions, calculate workday offsets, and look up tax filing deadlines. Tax and compliance answers should be checked against the relevant tax authority for the user's jurisdiction. <br>

### Deployment Geography for Use: <br>
Global, for mainland China calendar and tax-date questions. <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports that unsupported future-year queries may fetch public data and modify files inside the skill, including Python source. <br>
Mitigation: Review generated reference updates and script changes before use; run the scripts in a controlled workspace and keep versioned backups of trusted calendar data. <br>
Risk: The security evidence warns that tax-deadline guidance is under-scoped and that Beijing-only reference data may not match every jurisdiction. <br>
Mitigation: Verify tax deadlines with the relevant tax authority for the user's jurisdiction, and avoid relying on computed deadline output for compliance decisions. <br>
Risk: Future-year holiday or tax data may be unavailable or unconfirmed before official notices are published. <br>
Mitigation: Clearly label unconfirmed dates and verify them against State Council or tax authority publications before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linweibin6992-blip/cn-calendar) <br>
- [2025 mainland China holiday reference](references/holidays-2025.md) <br>
- [2026 mainland China holiday reference](references/holidays-2026.md) <br>
- [General tax filing calendar reference](references/tax-filing-calendar.md) <br>
- [2026 tax filing calendar reference](references/tax-filing-calendar-2026.md) <br>
- [NateScarlet holiday-cn data index](https://github.com/NateScarlet/holiday-cn) <br>
- [State Council 2025 holiday notice](https://www.gov.cn/zhengce/zhengceku/202411/content_6986383.htm) <br>
- [State Council 2026 holiday notice](https://www.gov.cn/zhengce/zhengceku/202511/content_7047091.htm) <br>
- [State Taxation Administration](https://www.chinatax.gov.cn/) <br>
- [12366 tax calendar API](https://12366.chinatax.gov.cn/bsfw/calendar/getCalendarListForMonth) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local reference files, run Python query scripts, and fetch public holiday or tax calendar data when local yearly data is unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
