## Description: <br>
Create, structure, and publish OpenClaw skills to ClawHub that pass the security scanner with clean ratings, including guidance for frontmatter schema, environment variable declarations, script safety, configuration changes, and publishing workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tdavis009](https://clawhub.ai/user/tdavis009) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill publishers use this guide to create, structure, validate, and publish OpenClaw skills on ClawHub. It is especially useful when preparing SKILL.md frontmatter, declaring credentials, reviewing script safety, documenting configuration changes, and iterating on scanner findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A copied trigger description can be too broad and cause generated skills to activate outside their intended tasks. <br>
Mitigation: Tighten each generated skill description and Use when clause to the exact tasks, services, and credentials the skill supports. <br>
Risk: An unreviewed skill directory can include secrets, personal data, generated artifacts, or unrelated files before publishing. <br>
Mitigation: Review the skill directory before using the publishing workflow, remove unrelated files, and verify scanner results after publication. <br>
Risk: Configuration examples can be applied incorrectly if treated as automatic changes. <br>
Mitigation: Treat configuration blocks as templates for manual review and require explicit approval before applying them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tdavis009/clawhub-skill-guide) <br>
- [Publisher Profile](https://clawhub.ai/user/tdavis009) <br>
- [Frontmatter Schema Reference](references/frontmatter-schema.md) <br>
- [Publish Workflow](references/publish-workflow.md) <br>
- [Scanner Compliance Deep Dive](references/scanner-compliance.md) <br>
- [Script Safety Patterns](references/script-safety.md) <br>
- [Basic Skill Template](assets/templates/basic-skill.md) <br>
- [Skill With Scripts Template](assets/templates/skill-with-scripts.md) <br>
- [Skill With Config Template](assets/templates/skill-with-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline YAML, JSON, and shell command examples plus reusable SKILL.md templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces documentation and templates for human review; it does not provide executable scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
