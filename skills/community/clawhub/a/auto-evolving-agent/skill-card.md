## Description: <br>
Self-evolving agent framework that uses hybrid Darwinian exploration and Lamarckian optimization to propose, score, and confirm improvements to an agent's skills, prompts, memory, and workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuqingsonga](https://clawhub.ai/user/zhuqingsonga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw developers use this skill to generate and compare multiple self-improvement proposals, review fitness scores and risks, and decide whether to update agent skills, prompts, memory, or workflows. It is intended for human-in-the-loop evolution rather than unattended self-modification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose changes to its own prompts, skills, memory, and behavior, which may cause unsafe or unwanted agent drift. <br>
Mitigation: Review every proposed diff or module change before approval and require explicit confirmation before applying self-modification. <br>
Risk: Automatic or scheduled evolution may trigger broad behavioral changes without a clear user request. <br>
Mitigation: Keep automatic and scheduled evolution disabled unless explicitly needed, and prefer user-initiated evolution sessions. <br>
Risk: Conversation details stored in memory or the gene pool may expose sensitive information. <br>
Mitigation: Avoid storing sensitive conversation content in memory or gene-pool records and review retained entries regularly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuqingsonga/auto-evolving-agent) <br>
- [Evolution History Template](references/evolution-history-template.md) <br>
- [Fitness Scoring Template](references/fitness-scoring-template.md) <br>
- [Gene Pool Template](references/gene-pool-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with ranked proposals, scoring tables, diffs, and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include candidate populations, fitness scores, risk levels, Git snapshot or rollback notes, and memory or gene-pool update records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
