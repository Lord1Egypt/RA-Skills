## Description:

Helps Flutter developers scaffold Hive local database services, repositories, and JSON-backed data models that follow Repository and MVVM patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[symboy](https://clawhub.ai/user/symboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill in Flutter projects to add Hive persistence, create repository classes, and generate data models with CRUD helpers from trusted entity JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted model JSON could cause unsafe Dart source generation or code injection beyond the intended model shape.

Mitigation: Use only entity JSON you wrote or fully trust, and inspect generated Dart files before building or shipping the app.

Risk: Generated files modify a Flutter project and may add persistence behavior that does not match the app's data model or compatibility needs.

Mitigation: Review the generated service, repository, model, and CRUD methods against the project schema and Hive initialization flow before use.

Risk: The security evidence says the generator should add stricter schema validation and path containment before routine use.

Mitigation: Treat installation and execution as review-required until the publisher adds stricter input validation and containment checks.

## Reference(s):

- [Flutter Hive Database skill page](https://clawhub.ai/symboy/skills/flutter-hive-database)
- [Generator script](scripts/generate.py)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated Dart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates Flutter project files under lib/ for Hive services, repositories, and models.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
