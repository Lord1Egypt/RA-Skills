## Description: <br>
查询上期所、大商所、郑商所、中金所、广期所期货实时行情及历史 K 线。当用户说：螺纹钢主力什么价？豆粕期货涨了吗？SC 原油最近一周走势？或类似期货行情问题时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve real-time and historical futures market data from JisuAPI for Shanghai, Dalian, Zhengzhou, China Financial Futures Exchange, and Guangzhou futures markets. It is intended for informational market-data lookup and summary, including single-contract queries and date-range historical K-line analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured JISU_API_KEY is sent to JisuAPI during futures data requests. <br>
Mitigation: Use a dedicated JisuAPI key with appropriate scope and rotate it if exposure is suspected. <br>
Risk: Market prices returned by the skill may be delayed, unavailable, or unsuitable as the sole basis for trading decisions. <br>
Mitigation: Use the data for informational lookup and verify important prices with an official source before acting. <br>
Risk: The script depends on python3 and the Python requests package being available in the runtime. <br>
Mitigation: Confirm the runtime includes python3 and requests before relying on the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/futures) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>
- [JisuAPI futures API documentation](https://www.jisuapi.com/api/futures/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the Python requests package, and JISU_API_KEY.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
