## Description: <br>
Provides standardized Node.js and TypeScript REST API development guidance using a layered Route, Controller, Service, Repository architecture with validation, DTO mapping, Prisma data access, and centralized error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bayudsatriyo](https://clawhub.ai/user/bayudsatriyo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, implement, refactor, and review backend REST API features with consistent layered architecture, validation, error handling, DTO mapping, and Prisma repository patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or copied route code could omit authorization checks or apply them at the wrong layer. <br>
Mitigation: Review authorization on every route and ensure service-level access rules match the product's security model before merging. <br>
Risk: Template hard-delete helpers and incomplete validation schemas could create destructive or under-validated API behavior if copied directly into production. <br>
Mitigation: Prefer soft-delete behavior where appropriate, tightly control destructive operations, and complete request validation schemas for each feature. <br>
Risk: The AppError and status handling contract may be inconsistent if the template is adapted mechanically. <br>
Mitigation: Verify the AppError, error-code, and centralized middleware contract in the target codebase before relying on generated error paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bayudsatriyo/backend-developer) <br>
- [Error Handling Pattern](references/error-handling.md) <br>
- [Senior Backend Engineer Mindset](references/senior-engineer-mindset.md) <br>
- [Utilities](references/utilities.md) <br>
- [Validation Pattern](references/validation.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with TypeScript code examples and implementation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing implementation patterns and code templates; generated application code should be reviewed before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
