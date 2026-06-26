## Description: <br>
调用多引擎（SearXNG 与 Tavily）抓取当日 AI 情报，执行去重、战略分级与洞察提炼，最终生成 5-9 条高管级 AI 日报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davyzhou1977-sketch](https://clawhub.ai/user/davyzhou1977-sketch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators, analysts, and teams use this skill to generate a concise Chinese AI news briefing for a target date. It supports manual use and scheduled daily runs when Tavily and, optionally, SearXNG search access are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outbound news searches may spend Tavily API quota and send query text to configured search services. <br>
Mitigation: Install only when this behavior is intended, configure approved Tavily and SearXNG endpoints, protect API keys, and monitor quota usage. <br>
Risk: Automatic daily execution can run without a human prompt, and run_daily.sh uses a hardcoded local proxy. <br>
Mitigation: Enable cron only for intended daily briefings, review or remove the proxy settings, and check logs after scheduled runs. <br>
Risk: Generated briefings can include stale or misleading news if source dates or search results are weak. <br>
Mitigation: Keep the skill's date checks and source links intact, and review the briefing before making operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davyzhou1977-sketch/ai-news-daily-zh) <br>
- [Publisher profile](https://clawhub.ai/user/davyzhou1977-sketch) <br>
- [Tavily](https://tavily.com) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Feishu card JSON with a Markdown body, or simplified Markdown when card output is unavailable.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 5-9 dated AI news items with title, category, linked source, summary, insight, and a short daily assessment.] <br>

## Skill Version(s): <br>
1.3.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
