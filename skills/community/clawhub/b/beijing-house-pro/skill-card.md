## Description: <br>
查询北京住宅小区的基础信息（房价/区域/交通），并通过官方验证渠道核实学区划片信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamhankai](https://clawhub.ai/user/iamhankai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to research Beijing residential communities, including price, district, transit signals, and school-zone verification steps. It supports housing research but requires current official confirmation before enrollment or purchase decisions. <br>

### Deployment Geography for Use: <br>
Beijing, China <br>

## Known Risks and Mitigations: <br>
Risk: User-entered community or address details may be sent to real-estate, search, and education websites. <br>
Mitigation: Use the skill only when comfortable sharing the searched community or address with those sites, and avoid providing unnecessary personal details. <br>
Risk: Housing prices, transit details, and school-zone policies can change and may be incomplete or stale. <br>
Mitigation: Verify school-zone and enrollment results with the current district education authority before making housing or enrollment decisions. <br>
Risk: Some official school-zone checks require personal login or QR-code authentication. <br>
Mitigation: Complete any authentication yourself in the browser and do not give the agent credentials, login tokens, or QR-login access. <br>
Risk: Web scraping and browser automation can fail because of CAPTCHA, site changes, or unavailable pages. <br>
Mitigation: Treat failed or partial lookups as inconclusive and use the official manual verification route when automation does not return a clear result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iamhankai/beijing-house-pro) <br>
- [Beike Beijing community search](https://bj.ke.com/xiaoqu/) <br>
- [Chaoyang official school-zone query](http://xqcx.bjchyedu.cn/) <br>
- [Beijing compulsory education enrollment platform](http://yjrx.bjedu.cn/) <br>
- [Haidian 17 school-district source](http://bj.bendibao.com/edu/2022425/313157.shtm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON results from helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require web search, browser-guided user verification, Chrome or Chromium, ChromeDriver, and network access to Beijing real-estate and education websites.] <br>

## Skill Version(s): <br>
1.0.8 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
