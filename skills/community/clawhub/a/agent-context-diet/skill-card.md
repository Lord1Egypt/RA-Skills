## Description:

Measures, splits, and verifies oversized agent skills and notes that consume context window budget.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vnbochkarev-netizen](https://clawhub.ai/user/vnbochkarev-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to measure context bloat from large skills or notes, split monolithic SKILL.md files into on-demand references, and verify that the split preserved content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the bulk skill-modification script lacks enough filesystem containment for safe installation without review.

Mitigation: Run the dry run first, set --root to a narrowly chosen skills folder, inspect target directories for symlinks, and review planned file writes before using --apply.

Risk: Rollback examples and cleanup commands can remove files if pointed at the wrong path.

Mitigation: Keep backups outside the skills root, list exact generated files before deleting anything, and avoid broad rm -rf commands during rollback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vnbochkarev-netizen/skills/agent-context-diet)
- [Measurement recipe](references/measurement-recipe.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Markdown, Configuration]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose filesystem changes to installed skill directories when the user chooses apply mode; dry-run and verification commands are part of the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and README report 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
