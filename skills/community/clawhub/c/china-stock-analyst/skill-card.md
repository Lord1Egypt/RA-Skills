## Description: <br>
A股短线营收分析助手，聚焦"短线交易信号+营收质量"双轨研判，8位专家并行分析，输出可复核证据链、双轨评分与明确交易条件 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjt0321](https://clawhub.ai/user/wjt0321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze A-share short-term opportunities, compare stocks, screen candidates, and verify historical stock reports using capital-flow, revenue-quality, risk, and evidence-chain checks. Outputs are research aids and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate trading-style suggestions for A-share stocks. <br>
Mitigation: Treat outputs as research only, preserve the not-advice disclaimer, and require human review before making investment decisions. <br>
Risk: The skill can use an East Money API key and send stock queries to East Money. <br>
Mitigation: Use a dedicated API key, keep it in environment variables or local ignored env files, and avoid submitting sensitive portfolio details or proprietary strategy text. <br>
Risk: Recent request and routing data may be retained locally by cache and quota files. <br>
Mitigation: Review local cache behavior before installation and clear local runtime files when query retention is not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wjt0321/china-stock-analyst) <br>
- [Valuation model reference](references/估值模型说明.md) <br>
- [Agent JSON schema standard](docs/agent-json-schema-standard.md) <br>
- [Agent teams blueprint](docs/agent-teams-blueprint.md) <br>
- [Report template](assets/报告模板.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with structured JSON expert outputs and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include timeliness warnings, source timestamps, evidence chains, dual-track scores, trading-condition labels, and not-advice disclaimers.] <br>

## Skill Version(s): <br>
2.4.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
