## Description: <br>
Domain Research Report Generator runs multi-angle deep research on a topic and produces a structured, decision-ready report with evidence-scored findings, divergences, key numbers, failed paths, and decision readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhihua-yang](https://clawhub.ai/user/zhihua-yang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to turn broad research, comparison, or update requests into saved Markdown reports with sourced claims, evidence strength labels, local-language search coverage, and decision guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics, queries, and source material may be sent to the configured web search provider. <br>
Mitigation: For sensitive work, invoke the skill explicitly and specify the desired region, language, source files, and acceptable save path; use a search provider appropriate for the data. <br>
Risk: Saved research reports may include sensitive findings or weakly supported claims if the topic is information-scarce. <br>
Mitigation: Review the evidence strength labels, source list, and research log before using the report for decisions, and choose a local save path suitable for the report contents. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhihua-yang/deep-researcher-pro) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/zhihua-yang) <br>
- [Evidence Scoring Criteria](references/evidence-scoring.md) <br>
- [Search Protocol](strategies/search-protocol.md) <br>
- [Decision Brief Template](templates/decision-brief.md) <br>
- [Comparison Template](templates/comparison.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Files] <br>
**Output Format:** [Structured Markdown report saved as a .md file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source citations, evidence strength labels, key numbers, failed paths, decision readiness, and a reproducibility research log.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
