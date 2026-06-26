## Description: <br>
Production-grade agent memory and quality system for multi-agent swarms that adds quality grading, progressive disclosure, orchestrator coordination, self-improvement protocols, and scoring templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DirtyRootsStudio](https://clawhub.ai/user/DirtyRootsStudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators managing multi-agent swarms use this skill to structure agent memory, audit SOUL.md quality, coordinate handoffs, and maintain lessons and patterns for ongoing improvement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports an autoreview helper that runs nested Codex review with full sandbox bypass by default. <br>
Mitigation: Review the autoreview helper before use, and run it with --no-yolo or AUTOREVIEW_YOLO=0 unless unrestricted local sandbox access is intentional. <br>
Risk: The skill directs agents to read and write workspace memory, lesson, pattern, scorecard, and handoff files, and orchestrators may read across agent workspaces. <br>
Mitigation: Limit access to intended agent workspaces and review generated or modified Markdown before using it for routing, audits, or operational decisions. <br>


## Reference(s): <br>
- [Clawhub Memory Tiers Pro release page](https://clawhub.ai/DirtyRootsStudio/clawhub-memory-tiers-pro) <br>
- [Required agent-memory-tiers skill](https://clawhub.ai/skills/agent-memory-tiers) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Files] <br>
**Output Format:** [Markdown guidance with checklists, rubrics, protocols, and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires agent-memory-tiers to be installed and configured first.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
