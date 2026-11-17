## Description:

Search, inspect, and progressively read open-access academic papers with the deepxiv CLI. Use when the user wants arXiv / PMC / Semantic Scholar paper search, paper triage, section-by-section reading, trending discovery, citation lookup, author background checks, baseline comparison, or literature review workflows without loading full papers too early.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xupeng8](https://clawhub.ai/user/xupeng8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research assistants use this skill to search, triage, read, and compare open-access academic papers while limiting context use through progressive reading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the external deepxiv CLI pulls the deepxiv-sdk Python package, which the security evidence flags as the main caution because it is unpinned.

Mitigation: Ask for user approval before installing, prefer a pinned and reviewed package version where possible, and verify Python 3.10+ plus deepxiv availability before use.

Risk: Some commands may contact literature, web-search, or LLM services, and the agent-query workflow can consume LLM account usage.

Mitigation: Tell the user before using web-search or LLM-agent workflows, get approval for LLM-agent cost, and prefer manual search plus targeted paper reads unless the question is genuinely open-ended.

## Reference(s):

- [Installing deepxiv](references/install.md)
- [DeepXiv Workflows](references/workflows.md)
- [Deepxiv Cli on ClawHub](https://clawhub.ai/xupeng8/skills/deepxiv-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown responses with command examples and optional JSON-derived summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concise paper summaries, comparison tables, section-reading notes, and explicit reading-rung provenance.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
