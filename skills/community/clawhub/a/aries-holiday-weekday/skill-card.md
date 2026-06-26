## Description: <br>
Query gov.cn Chinese holiday notices to determine workdays, holidays, and make-up workdays. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blueworld415](https://clawhub.ai/user/blueworld415) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check whether a specific date or every date in a month is a China workday, holiday, or weekend make-up workday using official gov.cn holiday notices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound web requests when yearly holiday data needs to be refreshed. <br>
Mitigation: Install only where outbound requests to the intended gov.cn sources are acceptable, and review network behavior before broader deployment. <br>
Risk: Security evidence reports an unrestricted URL-fetch helper and hardcoded government-search signing values that need review. <br>
Mitigation: Restrict notice fetching to HTTPS gov.cn hosts, remove or clearly document the captured signing material, and declare network and cache permissions explicitly. <br>
Risk: The skill writes yearly cache files as part of refresh behavior. <br>
Mitigation: Run it with appropriate workspace permissions and review generated cache data before relying on it for operational answers. <br>


## Reference(s): <br>
- [Gov Holiday Reference](references/api_reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/blueworld415/aries-holiday-weekday) <br>
- [2026 State Council Holiday Notice](https://www.gov.cn/gongbao/2025/issue_12406/202511/content_7048922.html) <br>
- [gov.cn Search Endpoint](https://sousuoht.www.gov.cn/athena/forward/2B22E8E39E850E17F95A016A74FCB6B673336FA8B6FEC0E2955907EF9AEE06BE) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown tables or structured text summaries, with Python helper code and CLI commands available for cache refreshes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-date results and month tables include date, weekday, workday status, kind, and holiday name when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
