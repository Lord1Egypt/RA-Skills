## Description: <br>
AI Growth Engine helps agents run a measurable self-improvement loop that reviews recent work, extracts patterns, plans adjustments, verifies results, and records learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingofzhao](https://clawhub.ai/user/kingofzhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent builders use this skill to give an agent a structured RAPVL growth cycle, Growth Score tracking, profession-specific metric presets, and periodic learning records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can shape agent behavior by producing growth recommendations and action plans that may be incorrect or poorly suited to the user's domain. <br>
Mitigation: Review Growth Score inputs, extracted failure patterns, and recommended plans before applying them to important workflows. <br>
Risk: The artifact describes recurring growth-history updates and periodic evolution reports, which may write files in the agent workspace. <br>
Mitigation: Run the skill in a scoped workspace and review expected log or report paths before enabling recurring use. <br>
Risk: Security evidence is clean, but the scanner guidance still recommends human review for unexpected credentials, file writes, background behavior, or external service use. <br>
Mitigation: Skim the installed files before use and keep normal skill review and scanning gates in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingofzhao/ai-growth-engine) <br>
- [Project homepage](https://github.com/KingOfZhao/AGI_PROJECT) <br>
- [A Survey of Self-Evolving Agents](https://arxiv.org/abs/2507.21046) <br>
- [SAGE: Multi-Agent Self-Evolution](https://arxiv.org/abs/2603.15255) <br>
- [Group-Evolving Agents](https://arxiv.org/abs/2602.04837) <br>
- [Self-evolving Embodied AI](https://arxiv.org/abs/2602.04411) <br>
- [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564) <br>
- [Beyond RAG for Agent Memory](https://arxiv.org/abs/2602.02007) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline formulas, configuration examples, Python snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to maintain growth logs, trend summaries, and evolution reports in a workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
