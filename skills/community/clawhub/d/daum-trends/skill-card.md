## Description: <br>
Daum real-time trends TOP10 briefing that extracts trending keywords from Daum and adds a representative news title for each keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garibong-labs](https://clawhub.ai/user/garibong-labs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and automation agents use this skill to fetch Korean real-time Daum search trends and format them for briefings, Telegram or Discord announcements, or scheduled trend monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Daum public trend and search pages at runtime. <br>
Mitigation: Allow outbound access only to the documented Daum endpoints and review network policy before deployment. <br>
Risk: The optional cron and announcement example can create recurring messages to a configured channel. <br>
Mitigation: Review the schedule, payload, and destination channel before enabling recurring delivery. <br>


## Reference(s): <br>
- [Daum homepage trend source](https://www.daum.net/) <br>
- [Daum search results endpoint](https://search.daum.net/search?w=tot&DA=RT1&rtmaxcoll=AIO,NNS,DNS&q=) <br>
- [ClawHub skill page](https://clawhub.ai/garibong-labs/daum-trends) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Plain text, Markdown, or HTML trend briefing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public Daum pages at runtime and does not require credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
