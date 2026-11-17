## Description:

Api Doc Gen generates API documentation from Flask, Django DRF, FastAPI, Express.js, NestJS, and generic code, with Markdown, OpenAPI 3.0, YAML, and Postman Collection outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API teams use this skill to inspect local API source files or code snippets and produce shareable API documentation and API client artifacts. It is aimed at keeping framework routes, inferred parameters, and response templates aligned with generated Markdown, OpenAPI, and Postman outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated documentation can expose internal API routes, parameter names, response shapes, and other implementation details.

Mitigation: Review generated Markdown, OpenAPI, YAML, and Postman files before publishing or sharing them outside the intended team.

Risk: Unpinned Python dependencies can change behavior or introduce supply-chain risk over time.

Mitigation: Install in a virtual environment and pin or lock dependency versions before production use.

Risk: Chinese-language CLI messages and documentation may be difficult for some operators to review accurately.

Mitigation: Have a fluent reviewer check generated output, logs, and usage instructions until locale support is available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/skills/api-doc-gen)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown, OpenAPI 3.0 JSON, OpenAPI 3.0 YAML, or Postman Collection JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write generated documentation to files or print it to standard output; batch mode writes one generated file per input source file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
