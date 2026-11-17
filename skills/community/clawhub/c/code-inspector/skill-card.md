## Description:

Code Inspector scans AI-generated code for common quality and security smells and reports findings with a production-readiness score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minirr890112-byte](https://clawhub.ai/user/minirr890112-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Python, JavaScript, and TypeScript files for heuristic AI-code quality issues such as truncation markers, hardcoded secrets, missing error handling, repeated code, incomplete imports, and bare except blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed package does not match several advertised checks.

Mitigation: Treat results as heuristic guidance and review the implementation and detected findings before relying on it as a release or deployment gate.

Risk: Installation instructions pull mutable code from GitHub without pinning a reviewed version.

Mitigation: Pin the reviewed commit or package artifact before installation, and re-run review when updating the source.

## Reference(s):

- [Code Inspector ClawHub listing](https://clawhub.ai/minirr890112-byte/skills/code-inspector)
- [Project homepage from Hermes metadata](https://github.com/minirr890112-byte/code-inspector)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Console text tables and optional JSON result output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports detected smell name, severity, line number, snippet, fix suggestion, and file quality score when available.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact frontmatter lists 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
