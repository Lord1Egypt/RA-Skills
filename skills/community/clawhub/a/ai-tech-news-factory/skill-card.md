## Description: <br>
AI全链路科技资讯工厂 coordinates trend tracking, RSS collection, knowledge-card creation, Xiaohongshu posts, and WeChat article publishing for AI technology news workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators, AI newsletter editors, and developer community operators use this skill to run a daily AI technology content pipeline from topic discovery through multi-platform drafts or publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can publish to real Xiaohongshu and WeChat accounts. <br>
Mitigation: Run step by step or in draft mode first, and review every generated post before allowing live publishing. <br>
Risk: Scheduled runs could repeatedly post content without a fresh human approval checkpoint. <br>
Mitigation: Avoid enabling cron for live posting unless an approval process and account safeguards are in place. <br>
Risk: Dependent local skills may handle cookies, sessions, authorization, and platform actions. <br>
Mitigation: Audit the dependent skills separately and restrict credentials to the minimum accounts and permissions needed. <br>
Risk: The default output path uses a root-level articles directory. <br>
Mitigation: Change outputs to a user-scoped directory before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zlszhonglongshen/ai-tech-news-factory) <br>
- [TechCrunch RSS feed](https://techcrunch.com/feed/) <br>
- [The Verge RSS feed](https://www.theverge.com/rss/index.xml) <br>
- [MIT News Artificial Intelligence RSS feed](https://news.mit.edu/topic/artificial-intelligence-rss) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, images] <br>
**Output Format:** [Markdown guidance, sample prompts, YAML configuration, cron shell command, JSON workflow data, article files, post records, and generated card images.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are organized under a dated articles directory and may include live platform publishing records when dependent publishing skills are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
