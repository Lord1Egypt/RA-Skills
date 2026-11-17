## Description:

A股逻辑可视化工具 turns finance or investment reasoning into Draw.io-compatible logic diagrams, including transmission chains, thesis maps, causal loops, and risk/benefit paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoeluli7459-dev](https://clawhub.ai/user/zoeluli7459-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-focused agents use this skill to convert structured or semi-structured investment logic into visual diagrams. It is suited for explaining causal chains, thesis maps, and risk/benefit paths, not for stock screening, news lookup, or signal tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML diagram files load viewer JavaScript from diagrams.net.

Mitigation: Open generated HTML only from trusted inputs and review files before sharing or deploying them.

Risk: The renderer can write HTML files to caller-provided paths.

Mitigation: Constrain filenames to a dedicated artifact directory and avoid privileged or unrelated paths.

Risk: Investment relationships in diagrams can appear authoritative even when source reasoning is incomplete.

Mitigation: Require supporting logic for causal links and mark uncertain relationships as assumptions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoeluli7459-dev/skills/alphaear-logic-visualizer)
- [Draw.io XML generation prompts](references/PROMPTS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration]

**Output Format:** [Markdown responses with Draw.io mxGraph XML or generated HTML diagram file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated diagrams use color-coded positive, negative, and neutral nodes and may embed Draw.io viewer configuration in HTML output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
