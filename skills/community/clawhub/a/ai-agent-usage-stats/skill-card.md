## Description: <br>
选择要监控的 AI 助手 → 查看 token 消耗。支持 Hermes / Claude Code / CodeX / OpenClaw，每次都让你选 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huyiling1111](https://clawhub.ai/user/huyiling1111) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI-agent users use this skill to inspect local token usage, cache usage, estimated costs, and activity trends for supported local assistants. It is intended for local usage review, monitoring, comparison, and export workflows rather than upstream billing reconciliation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local AI-agent usage stores, including logs and databases for supported assistants. <br>
Mitigation: Install and run it only on machines where local agent usage data may be inspected, and review the documented data sources before use. <br>
Risk: The setup workflow can modify PATH and create a local command wrapper. <br>
Mitigation: Review the setup step before running it, and use update or uninstall commands only when those local changes are intended. <br>
Risk: Displayed token and cost totals are local estimates and may differ from upstream provider billing. <br>
Mitigation: Use the output as a local usage ledger, and compare against provider billing systems for financial reconciliation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huyiling1111/ai-agent-usage-stats) <br>
- [Publisher profile](https://clawhub.ai/user/huyiling1111) <br>
- [README](README.md) <br>
- [English README](README.en.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with command examples and local usage summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include token totals, cache metrics, call counts, estimated costs, comparisons, live-monitoring deltas, and export guidance.] <br>

## Skill Version(s): <br>
2.6.1 (source: server release metadata, SKILL.md frontmatter, and CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
