## Description:

Generate high-quality EvoMap bundles from real skills with actual code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephyb97](https://clawhub.ai/user/josephyb97)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to scan local OpenClaw skills and generate EvoMap Gene, Capsule, and EvolutionEvent bundles that include source-derived snippets and strategy steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated bundles can copy local skill metadata and source snippets into publishable JSON files.

Mitigation: Run the skill only in workspaces intended for export and review generated JSON before sharing or publishing.

Risk: Bulk generation can process many local skills, including skills from sensitive workspaces.

Mitigation: Avoid the bulk command in sensitive workspaces and generate from specific reviewed skills when possible.

Risk: Generated confidence, success, and production-tested claims may not represent real validation evidence.

Mitigation: Treat these claims as generated metadata and verify them independently before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josephyb97/skills/evomap-skills-wrapper)

## Skill Output:

**Output Type(s):** [JSON, Code, Shell commands, Guidance]

**Output Format:** [JSON files with Gene, Capsule, and EvolutionEvent objects, plus command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated bundles can include copied source snippets and confidence or success metadata that should be reviewed before sharing.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
