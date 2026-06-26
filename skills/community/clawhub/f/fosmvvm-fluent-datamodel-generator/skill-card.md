## Description: <br>
Generate Fluent DataModels for FOSMVVM server-side persistence, including models, migrations, and tests for database-backed entities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foscomputerservices](https://clawhub.ai/user/foscomputerservices) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold Swift Fluent persistence-layer code for FOSMVVM/Vapor projects. It helps create DataModels, schema and seed migrations, relationship patterns, migration registration guidance, and field tests for database-backed entities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated migrations, raw SQL, seed data, foreign keys, cascade deletes, or revert behavior can affect application databases. <br>
Mitigation: Review all generated database changes before committing or running them, especially against shared, staging, or production databases. <br>
Risk: Using the skill outside Fluent/Vapor projects can produce inappropriate persistence-layer code. <br>
Mitigation: Confirm Fluent indicators such as Fluent package dependencies, Fluent imports, property wrappers, or existing migrations before using the generated output. <br>
Risk: Generated code and migration registration may need adaptation to local project structure and conventions. <br>
Mitigation: Compare the output with existing project models, migrations, and tests, then run the project test suite before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/foscomputerservices/fosmvvm-fluent-datamodel-generator) <br>
- [FOSUtilities homepage](https://github.com/foscomputerservices/FOSUtilities) <br>
- [Reference templates](reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with Swift code blocks and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for Fluent/Vapor projects and may include database-impacting migration and seed templates.] <br>

## Skill Version(s): <br>
2.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
