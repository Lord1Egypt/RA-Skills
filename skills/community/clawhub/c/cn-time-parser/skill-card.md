## Description: <br>
Parses Chinese natural-language time expressions into concrete Gregorian dates, millisecond timestamps, lunar-calendar details, and holiday or workday indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[as3long](https://clawhub.ai/user/as3long) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract Chinese time phrases from user requests, convert them to dates or timestamps, and check lunar-calendar festivals, public holidays, and workday status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on npm packages for date, lunar-calendar, and holiday logic. <br>
Mitigation: Install from the included lockfile and review dependency updates before deployment. <br>
Risk: Broad Chinese time-related triggers may send more user text than necessary to the parser. <br>
Mitigation: Pass only the text needed for time parsing. <br>
Risk: Relative dates and timestamps depend on the runtime system clock. <br>
Mitigation: Verify the execution environment's date, time, and timezone before relying on parsed results. <br>


## Reference(s): <br>
- [Supported time keywords](references/time-keywords.md) <br>
- [ClawHub skill page](https://clawhub.ai/as3long/cn-time-parser) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with inline shell command examples; script output is JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dates are calculated from the current system time, and timestamps are Unix time in milliseconds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
