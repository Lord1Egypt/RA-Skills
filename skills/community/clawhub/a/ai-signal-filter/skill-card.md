## Description: <br>
从海量 AI 动态中筛选真正有决策价值的信号，并为每条信号回答“所以呢”和“该做什么”。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ah0210](https://clawhub.ai/user/ah0210) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, founders, and analysts use this skill to monitor AI industry changes, filter noisy updates, and produce decision-oriented signal reports with source URLs, confidence levels, and concrete actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Profile watchlists and custom keywords may be used in web searches and passed to a temporary subagent. <br>
Mitigation: Review memory/signal/profile.md before use and remove sensitive companies, projects, or keywords. <br>
Risk: The skill can create or update local signal history for personalization and deduplication. <br>
Mitigation: Periodically review or delete memory/signal/history.md when persistent local history is not desired. <br>
Risk: AI-generated market or industry signals can be incomplete, stale, or misleading despite source and confidence checks. <br>
Mitigation: Verify high-impact recommendations against primary sources before making business, product, or investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ah0210/ai-signal-filter) <br>
- [Output format](references/output-format.md) <br>
- [Quality gates](references/quality-gates.md) <br>
- [Search strategy](references/search-strategy.md) <br>
- [GitHub Trending](https://github.com/trending) <br>
- [Hacker News](https://news.ycombinator.com/) <br>
- [Reddit LocalLLaMA feed](https://www.reddit.com/r/LocalLLaMA/hot/.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown report with execution metadata, source URLs, confidence labels, and action recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local memory/signal/history.md and, after user confirmation, save signal/{date}-report.md.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
