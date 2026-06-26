## Description: <br>
Content search and synthesis primitive for Twitter/X and News sources using Kaito search tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YH9277](https://clawhub.ai/user/YH9277) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search crypto-related Twitter/X and News content by token, keyword, topic, or username, then synthesize relevant findings with source links. It is intended for content discovery and summary, not mindshare tracking, sentiment analysis, or user profiling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search topics are sent to the configured Kaito MCP service and may reveal sensitive interests or research topics. <br>
Mitigation: Do not include secrets, private account details, wallet-sensitive information, or confidential research in search queries. <br>
Risk: Synthesized search results can be incomplete or misleading when retrieved source material is thin or ambiguous. <br>
Mitigation: Verify important claims against the returned tweet or news URLs before relying on them. <br>


## Reference(s): <br>
- [Crypto Search release page](https://clawhub.ai/YH9277/crypto-search) <br>
- [YH9277 publisher profile](https://clawhub.ai/user/YH9277) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summary with categorized findings, source URLs, and smart_engagement counts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Standalone output is grouped by Twitter sentiment categories and News results; workflow use can return structured search results for composition.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
