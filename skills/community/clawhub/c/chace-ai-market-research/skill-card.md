## Description: <br>
Automates end-to-end market research by coordinating crawl4ai-style collection, trend monitoring, structured product research, historical comparison, and report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ling-qian](https://clawhub.ai/user/ling-qian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and market researchers use this skill to generate competitive, trend, product, and market scans from a topic and optional source URLs. It is intended to produce structured reports and supporting artifacts for recurring market intelligence workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-research topics, summaries, reports, and source-derived findings may be saved locally or in agentmemory. <br>
Mitigation: Avoid confidential topics unless persistence is acceptable; disable or review memory writes and remove stored findings when retention is not desired. <br>
Risk: Scheduled WeChat or channel delivery can disclose generated reports to an unintended destination. <br>
Mitigation: Verify the delivery target and require human review before enabling scheduled or automatic external delivery. <br>
Risk: Several advertised integrations are early-stage, simulated, or not fully implemented in the artifact. <br>
Mitigation: Test the skill in a non-production workspace and inspect generated reports and artifacts before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ling-qian/chace-ai-market-research) <br>
- [Declared homepage](https://github.com/yourusername/ai-market-research-skill) <br>
- [README](artifact/README.md) <br>
- [Requirements](artifact/Requirements.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with generated artifact files and optional JSON or HTML output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Depth controls affect source count, runtime, and token usage; optional history comparison can read and write agentmemory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, SKILL.md frontmatter, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
