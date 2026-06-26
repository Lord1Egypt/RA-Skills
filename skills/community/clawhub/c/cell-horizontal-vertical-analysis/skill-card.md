## Description: <br>
Deep-research skill for Chinese outputs using 横纵分析 / Horizontal-Vertical Analysis. Use when Codex needs to systematically study a product, company, concept, technology, market, or person: rebuild the full life-cycle on a vertical timeline, compare current peers or substitutes on a horizontal slice, cross the two axes into original insight, separate facts from inferences, and deliver a structured report or optional PDF. Not for quick definitions, gossip, or unsupported legal / investment due diligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cellinlab](https://clawhub.ai/user/cellinlab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to produce structured Chinese research reports about products, companies, concepts, technologies, markets, or people. It guides the agent through scoping, source mapping, vertical timeline analysis, horizontal comparison, and synthesis while separating facts, inferences, and unknowns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF generation may fail when local Python dependencies are missing. <br>
Mitigation: Install the documented Markdown and PDF dependencies before export, or deliver the Markdown report and note the missing dependency. <br>
Risk: The skill defaults to Chinese output, which may not fit all readers. <br>
Mitigation: Specify a different output language when invoking the skill. <br>
Risk: Research conclusions can be misleading if the source map is incomplete or core facts are weakly supported. <br>
Mitigation: Use the built-in source strategy, double-check key facts, and keep facts, inferences, and unknowns separate. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Source Strategy](references/source-strategy.md) <br>
- [Analysis Lenses](references/analysis-lenses.md) <br>
- [Report Contract](references/report-contract.md) <br>
- [Research Schema](references/research-schema.json) <br>
- [Research Report Template](assets/research-report-template.md) <br>
- [OpenClaw homepage](https://github.com/cellinlab/cell-skills/tree/main/skills/horizontal-vertical-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research report with optional PDF export guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to Chinese output; supports quick, standard, and deep report modes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
