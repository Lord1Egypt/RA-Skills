## Description:

Generate complete django-vue-admin style CRUD code including Django models, serializers, views, URLs, Vue API, and Vue pages from module descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpzhengcn](https://clawhub.ai/user/jpzhengcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building django-vue-admin applications use this skill to turn module and field descriptions into Django REST Framework and Vue CRUD code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated admin and security code may include unsafe authorization paths and a default password pattern.

Mitigation: Use the skill in a disposable branch or sandbox, fix object-permission behavior, remove the 0000 default password, and test authentication, authorization, and destructive CRUD actions before merging.

Risk: The generator writes derived backend and frontend files from module names and paths.

Mitigation: Validate module names and output paths, avoid automatic overwrites, and review generated files before committing them.

## Reference(s):

- [Skill overview and usage](SKILL.md)
- [Core module templates](templates/CORE_MODULES.md)
- [Business logic reference](templates/BUSINESS_LOGIC.md)
- [Logic flow reference](templates/LOGIC_FLOW.md)
- [Field template reference](templates/FIELD_TEMPLATE.md)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with Python, JavaScript, Vue, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces generated CRUD code and setup guidance that should be reviewed before applying to a project.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
