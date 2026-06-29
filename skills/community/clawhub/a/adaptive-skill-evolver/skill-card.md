## Description: <br>
Skill Evolver analyzes agent execution traces, generates evidence-scored Evolution Units, and can attach durable lessons to skills so agents adapt from prior use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polkalian](https://clawhub.ai/user/polkalian) <br>

### License/Terms of Use: <br>
MIT No Attribution <br>


## Use Case: <br>
Developers and agent operators use this skill to review how skills perform in real sessions, turn recurring lessons into reusable guidance, and manage which lessons are attached to each skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect agent session logs and persist derived trace or evolution history. <br>
Mitigation: Install only in environments where session-log review is acceptable, and review retained state/history files according to local data-handling policy. <br>
Risk: The skill can send trace, unit, or skill text to the configured model provider. <br>
Mitigation: Set privacy.allowRemoteLLM to false for sensitive environments, or configure an approved model endpoint before enabling generation, validation, or review. <br>
Risk: The skill can update other skills' SKILL.md files with generated guidance. <br>
Mitigation: Use manual mode or review generated Evolution Units before inlining; evict or block units and skills that should not be modified. <br>
Risk: Automatic scheduling may run evolution cycles without direct user initiation. <br>
Mitigation: Avoid enabling scheduling until setup and scheduling configuration are reviewed, and prefer manual mode when unattended runs are not appropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/polkalian/adaptive-skill-evolver) <br>
- [README](README.md) <br>
- [Skill Instructions](SKILL.md) <br>
- [Brief Report Prompt](brief-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, JSON status/configuration data, shell commands, and concise text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and an Agent Skills-compatible platform with JSONL session logs.] <br>

## Skill Version(s): <br>
2.4.13 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
