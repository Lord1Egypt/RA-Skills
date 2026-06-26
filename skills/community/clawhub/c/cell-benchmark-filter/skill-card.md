## Description: <br>
Benchmark filtering for Chinese creator, OPC, and one-person-business work. Use when Codex needs to judge whether a person, creator, or business is actually worth studying; separate business signal from vanity signal; decide what layer is worth copying; and recommend whether to stop at a shortlist or hand the target to $opc-case-research for deeper study. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cellinlab](https://clawhub.ai/user/cellinlab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to screen Chinese creator, OPC, and one-person-business benchmarks before investing in deeper case research. It helps identify the copyable layer, separate business signal from vanity signal, and choose a concrete next move. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for quick benchmark filtering rather than full case research. <br>
Mitigation: Use its output as an initial screen and escalate strong benchmarks to deeper case research when the decision requires more evidence. <br>
Risk: The skill may answer in Chinese by default. <br>
Mitigation: Set the desired response language explicitly when a non-Chinese output is required. <br>
Risk: Benchmark judgments can be misleading if based on private or unsupported data. <br>
Mitigation: Base decisions on public, reviewable signals and avoid relying on private data unless the user has permission to use it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cellinlab/cell-benchmark-filter) <br>
- [Project homepage](https://github.com/cellinlab/cell-skills/tree/main/skills/benchmark-filter) <br>
- [五层筛选框架](references/filter-framework.md) <br>
- [模仿颗粒度检查](references/copy-granularity.md) <br>
- [对标筛选卡](assets/benchmark-card-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown benchmark-filter card, usually in Chinese] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a one-line judgment, five-filter result, worth-learning layers, do-not-copy layers, first move, and escalation recommendation.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
