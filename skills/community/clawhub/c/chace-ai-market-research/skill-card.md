## Description:

Automates end-to-end market research by combining web crawling, trend monitoring, structured product analysis, and optional historical memory comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ling-qian](https://clawhub.ai/user/ling-qian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market research users can use this skill to gather source material, monitor trends, compare prior findings, and generate structured market research reports for competitive, industry, product launch, or investment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may be written outside the intended output folder.

Mitigation: Run the skill only in a constrained workspace or sandboxed OpenClaw process until report path handling is fixed and reviewed.

Risk: Research topics, source URLs, summaries, and findings may be saved locally or to agentmemory.

Mitigation: Avoid sensitive internal topics and sources unless local report storage and memory persistence have been approved for that data.

Risk: Optional channel delivery and cron examples can distribute generated reports beyond the local workspace.

Mitigation: Review delivery destinations and report contents before enabling scheduled or WeChat/channel delivery.

Risk: The artifact behavior is currently mock/demo-like for crawl4ai, trendradar, and product-research integrations.

Mitigation: Treat outputs as draft research guidance and verify claims against primary sources before using them for business decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ling-qian/skills/chace-ai-market-research)
- [Publisher Profile](https://clawhub.ai/user/ling-qian)
- [Declared Homepage](https://github.com/yourusername/ai-market-research-skill)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with optional JSON-style artifacts and setup or troubleshooting commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports quick, standard, and deep research depths; output may include local report files, crawl summaries, trend summaries, analysis results, and optional memory entries.]

## Skill Version(s):

0.1.0 (source: frontmatter, changelog, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
