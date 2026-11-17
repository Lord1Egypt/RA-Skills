## Description:

Integrate Didit Database Validation API to verify personal data against government databases for national ID, identity-document, and identity database checks across supported Latin American countries and Spain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:


## Use Case:

Developers and identity operations teams use this skill to integrate Didit's database-validation API, validate government-issued identifiers, and interpret match outcomes for supported countries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided identity details to Didit's verification API, which can include sensitive personal data.

Mitigation: Use it only with appropriate consent or another lawful basis, avoid logging full identifiers or dates of birth, and share only data required for the validation request.

Risk: API credentials are required to call Didit's service.

Mitigation: Use a dedicated DIDIT_API_KEY, store it in the environment or a secret manager, rotate it when needed, and do not commit it to skill files or logs.

Risk: The bundled utility script depends on Python requests and makes outbound HTTPS calls.

Mitigation: Install dependencies in an isolated environment with pinned versions where possible and review outbound API behavior before deployment.

## Reference(s):

- [Didit Documentation](https://docs.didit.me)
- [Didit Database Validation API Reference](https://docs.didit.me/standalone-apis/database-validation)
- [Didit Database Validation Feature Guide](https://docs.didit.me/core-technology/database-validation/overview)
- [Didit Database Validation Supported Countries](https://docs.didit.me/core-technology/database-validation/database-validation-supported-countries)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON, Python, TypeScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API payloads, response-handling guidance, and command-line validation examples that require DIDIT_API_KEY.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
