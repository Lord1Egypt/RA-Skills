## Description:

Builds and applies evidence-based labeling taxonomies for patents, scientific literature, product materials, technical intelligence, customer requirements, and other structured text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, patent analysts, research analysts, and operations teams use this skill to design, pilot, validate, and run evidence-backed labeling workflows with open, semi-open, or closed taxonomies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected query terms, record excerpts, or patent/literature identifiers may be sent to the PatSnap/Zhihuiya MCP service during evidence enhancement.

Mitigation: Configure MCP deliberately, avoid pasting API keys into chat, use selective lookup, and record service/tool provenance for external evidence calls.

Risk: Incorrect taxonomy definitions or boundary decisions can produce misleading labels when applied across a full dataset.

Mitigation: Use the scope, freeze, and execution confirmation gates; pilot before full runs; and route low-confidence, incomplete, or conflicting cases to review.

Risk: Full-run outputs can be incomplete or invalid if source IDs, taxonomy paths, evidence excerpts, or workbook sheets are inconsistent.

Mitigation: Run the included validation helpers for task configuration, taxonomy structure, and labeling workbooks before delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/evidence-based-labeling)
- [Setup Guide](README.md)
- [Workflow Modes](references/workflow-modes.md)
- [Input and Output Contract](references/input-output-contract.md)
- [Default Decision Rules](references/default-decision-rules.md)
- [Taxonomy Design](references/taxonomy-design.md)
- [Quality and Review](references/quality-and-review.md)
- [Zhihuiya MCP Orchestration](references/zhihuiya-mcp-orchestration.md)
- [PatSnap MCP service marketplace](https://open.zhihuiya.com/marketplace/mcp-servers)
- [PatSnap developer authentication guide](https://open.zhihuiya.com/devportal/guides/authentication)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance, JSON validation reports, CSV/XLSX workbooks, YAML/CSV configuration templates, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include source records with added labeling fields, evidence tables, taxonomy backlog, review queues, QA summaries, task metadata, and MCP provenance without storing credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
