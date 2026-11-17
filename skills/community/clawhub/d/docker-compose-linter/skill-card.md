## Description:

Lint docker-compose.yml files for security, best practices, and port conflicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze Docker Compose files for security findings, operational best-practice gaps, service inventory, and port conflicts before local or CI deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports can expose secret-like values from Docker Compose environment entries.

Mitigation: Avoid running on production Compose files in shared logs and redact secret findings before publishing output.

Risk: The custom YAML parser may miss valid Compose constructs, so clean results can be incomplete.

Mitigation: Treat results as advisory and pair them with review or a standards-based Compose parser for release gates.

Risk: The security evidence reports a suspicious verdict because reliability limits are overstated.

Mitigation: Review findings manually before relying on them in CI or deployment decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Text, JSON, or Markdown reports with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports lint, services, ports, and audit commands with severity filtering, ignored rules, and strict CI exit behavior.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
