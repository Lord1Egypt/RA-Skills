## Description: <br>
Aiwencai helps agents query Tonghuashun/Iwencai financial and economic data across securities, funds, futures, bonds, macro indicators, shareholder information, ratings, and global markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liliangjie91](https://clawhub.ai/user/liliangjie91) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and financial-data users use this skill to turn natural-language finance questions into Iwencai API queries and return structured financial results for agent responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial queries are sent to Iwencai/Tonghuashun using the user's API key. <br>
Mitigation: Keep IWENCAI_API_KEY in a secret or environment variable and avoid sending account numbers, personal identifiers, or confidential portfolio details. <br>
Risk: Financial results may be incomplete, stale, or unsuitable as the sole basis for decisions. <br>
Mitigation: Verify important financial results against trusted sources before relying on them. <br>


## Reference(s): <br>
- [Aiwencai ClawHub release](https://clawhub.ai/liliangjie91/aiwencai) <br>
- [API reference](references/api.md) <br>
- [Build requirements](references/requirement.md) <br>
- [Iwencai query API](https://openapi.iwencai.com/v1/query2data) <br>
- [Iwencai web query fallback](https://www.iwencai.com/unifiedwap/chat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API or CLI results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IWENCAI_API_KEY; query, page, limit, and cache options affect returned financial records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
