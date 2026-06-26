## Description: <br>
Distill successful workflows into reusable skills with quality gates, including novelty, success, reuse potential, grounding, IP boundary checks, trigger discipline, and pre-publish vetting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christianye](https://clawhub.ai/user/christianye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill after completing complex multi-step work to decide whether to create, update, stage, or skip a reusable skill. It guides extraction, generalization, quality checks, IP review, and public registry preparation for SKILL.md-style releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or updated skill content can introduce incorrect or misleading guidance if accepted without review. <br>
Mitigation: Review generated SKILL.md, memory notes, and registry entries before relying on them or publishing them. <br>
Risk: Automatic distillation can create local files in workflows where file creation should require an explicit command. <br>
Mitigation: Avoid enabling automatic distillation in those workflows, or require explicit user confirmation before writing files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/christianye/auto-skill-distiller) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with example SKILL.md frontmatter and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or update SKILL.md content, memory notes, registry entries, and review checklists for human validation.] <br>

## Skill Version(s): <br>
2.0.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
