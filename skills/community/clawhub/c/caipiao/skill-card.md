## Description: <br>
查彩票分类、最新与历史开奖、号码是否中奖等。当用户说：双色球最新开奖号码？大乐透上期结果？或类似彩票开奖问题时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve lottery categories, latest or historical drawing results, and winning-status checks from JisuAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: JisuAPI receives the configured API key and user-requested lottery query details, including ticket numbers used for prize checks. <br>
Mitigation: Use a dedicated limited JisuAPI key and avoid submitting sensitive ticket information unless sharing it with JisuAPI is acceptable. <br>
Risk: Lottery lookups may consume JisuAPI account quota. <br>
Mitigation: Monitor provider quota and configure limits on the API key where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/caipiao) <br>
- [JisuAPI lottery API documentation](https://www.jisuapi.com/api/caipiao/) <br>
- [JisuAPI provider homepage](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON results and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; results depend on JisuAPI availability, account access, and quota.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
