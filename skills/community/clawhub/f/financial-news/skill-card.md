## Description: <br>
A financial-news monitoring skill that presents sample workflows for querying finance news, setting watch alerts, and classifying news sentiment. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[alsoforever](https://clawhub.ai/user/alsoforever) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this demo skill to understand a financial-news monitoring workflow and generate sample Python calls or console-style output for news queries, watch setup, and sentiment classification. It should not be relied on for current financial news, investment alerts, sentiment analysis, or trading decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises live financial-news aggregation, alerts, and sentiment analysis, but the reviewed artifact behaves as a placeholder demo. <br>
Mitigation: Treat outputs as examples only and verify all financial news, alerts, sentiment, and investment implications with authoritative external sources. <br>
Risk: The artifact declares an optional TUSHARE_TOKEN even though reviewed code does not implement live Tushare data access. <br>
Mitigation: Do not provide API tokens unless a later reviewed version clearly implements live access and explains what data is sent, stored, and notified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alsoforever/financial-news) <br>
- [Publisher profile](https://clawhub.ai/user/alsoforever) <br>
- [Skill homepage](https://aigogoai.com) <br>
- [Finance news sources](https://aigogoai.com/knowledge/news-sources) <br>
- [News sentiment analysis](https://aigogoai.com/knowledge/sentiment-analysis) <br>
- [News trading strategy](https://aigogoai.com/knowledge/news-trading) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python snippets and terminal-style text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and pip; TUSHARE_TOKEN is declared optional, but the reviewed artifact does not implement live Tushare access.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
