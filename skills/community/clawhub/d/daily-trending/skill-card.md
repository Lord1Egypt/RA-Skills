## Description: <br>
获取今日热榜，从tophub.today抓取各平台热搜榜单。当用户询问"今天有什么热搜"、"热榜"、"微博热搜"时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Enchograph](https://clawhub.ai/user/Enchograph) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users invoke this skill to get a concise daily summary of important trending topics from Chinese web platforms. It helps readers quickly identify policy, social, business, and discussion-worthy news items while filtering out entertainment noise and advertising. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts tophub.today at runtime to fetch public trending-topic pages. <br>
Mitigation: Use it only in environments where outbound web access to TopHub is acceptable. <br>
Risk: The final summary intentionally omits source labels and may compress or omit context from individual trend pages. <br>
Mitigation: Verify important news against primary sources before acting on it or sharing it as authoritative. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Enchograph/daily-trending) <br>
- [TopHub Weibo hot search](https://tophub.today/n/KqndgxeLl9) <br>
- [TopHub Zhihu hot list](https://tophub.today/n/mproPpoq6O) <br>
- [TopHub Baidu real-time hot topics](https://tophub.today/n/Jb0vmloB1G) <br>
- [TopHub 36Kr 24-hour hot list](https://tophub.today/n/Q1Vd5Ko85R) <br>
- [TopHub Huxiu hot articles](https://tophub.today/n/5VaobgvAj1) <br>
- [TopHub The Paper hot list](https://tophub.today/n/wWmoO5Rd4E) <br>
- [TopHub 52pojie daily hot posts](https://tophub.today/n/NKGoRAzel6) <br>
- [TopHub Hupu pedestrian street hot posts](https://tophub.today/n/G47o8weMmN) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style ranked list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces five concise news-style trending-topic items without source labels.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
