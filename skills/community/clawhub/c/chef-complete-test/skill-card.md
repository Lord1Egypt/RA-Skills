## Description:

Generates structured Chinese recipe guidance through a chef-perspective drafting, AI review, and optimized final recipe workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[puppetcat-fire](https://clawhub.ai/user/puppetcat-fire)

### License/Terms of Use:

MIT-0

## Use Case:

External users and OpenClaw agents use this skill to generate detailed cooking guidance for requested dishes, including chef-style steps, review notes, and an optimized recipe output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local shell installer runs with the user's privileges and may create files in the skill directory or copy the package into an OpenClaw skills folder.

Mitigation: Review install.sh before installation and run it only in an environment where these local file changes are acceptable.

Risk: The package appears incomplete, so the documented chef-dialog.sh workflow is likely to fail unless missing scripts are supplied.

Mitigation: Verify that required workflow scripts are present before installing or invoking the skill.

Risk: Generated cooking guidance can be unsuitable for a user's equipment, food safety needs, allergies, or dietary restrictions.

Mitigation: Have a knowledgeable user review recipe outputs before following them, especially for safety-critical steps and ingredient substitutions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/puppetcat-fire/skills/chef-complete-test)
- [ClawHub publisher profile](https://clawhub.ai/user/puppetcat-fire)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance, Files]

**Output Format:** [Markdown recipe guidance with shell-command installation and generated recipe files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documented outputs include chef-perspective recipes, analysis reports, optimized recipes, and summary Markdown files under an output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
