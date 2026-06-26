## Description: <br>
自动搜索携程酒店，支持实时比价和详情获取。使用浏览器自动化技术，实现携程账号登录、酒店搜索、详情获取和对比分析功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexfeng75](https://clawhub.ai/user/alexfeng75) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers, travel planners, and developers use this skill to automate Ctrip hotel searches by city, dates, price range, and lodging type, then compare hotel details, reviews, and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to store Ctrip account credentials in plaintext configuration. <br>
Mitigation: Use a dedicated or low-risk Ctrip account, keep config.json local, do not commit or share it, and prefer environment variables or a local secret manager when adapting the skill. <br>
Risk: Some included Python helper scripts can route hotel search queries through Maton/Brave instead of Ctrip. <br>
Mitigation: Review those scripts before use, set MATON_API_KEY only when that route is intended, and assume submitted queries may leave the local environment. <br>
Risk: Demo hotel recommendations and example search results may be outdated or unverified. <br>
Mitigation: Confirm hotel availability, prices, ratings, policies, and booking terms directly on Ctrip or another trusted booking source before acting on recommendations. <br>
Risk: Browser automation may encounter CAPTCHA prompts or break when Ctrip changes page structure. <br>
Mitigation: Expect manual login verification when prompted, keep selectors under review, and validate search results after dependency or site changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexfeng75/ctrip-hotel-search) <br>
- [README](artifact/README.md) <br>
- [Usage guide](artifact/USAGE.md) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON-like JavaScript result objects with hotel lists, comparisons, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require Ctrip credentials, Playwright browser installation, manual CAPTCHA completion, and optional MATON_API_KEY for Maton/Brave helper scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
