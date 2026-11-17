## Description:

ClawHub Retry & Fallback helps ClawHub Agent tasks retry failed tool calls, classify exceptions, switch to configured fallback tools, degrade task execution, and record audit logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add retry, fallback, degradation, and audit logging behavior around ClawHub Agent tool calls and workflow steps. It is intended for operational resilience when transient failures, unavailable services, or partially failed task chains need controlled handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence flags the release as suspicious because audit export behavior, unpinned install dependencies, and unsupported security claims need review before installation.

Mitigation: Install in an isolated virtual environment, pin and hash dependencies, and review the claimed security and compliance properties before deployment.

Risk: Fallback tool configuration can redirect work to backup functions and map parameters, which can change task behavior.

Mitigation: Restrict who can configure fallback tools and require explicit confirmation for sensitive or high-impact fallback paths.

Risk: Audit logs and CSV/XLSX exports may contain task details or other sensitive operational data.

Mitigation: Treat audit logs and exports as sensitive, limit access to them, and avoid opening spreadsheet exports from untrusted task data until formula neutralization is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiyuelv/skills/clawhub-retry-fallback)
- [README](artifact/README.md)
- [Retry policy configuration](artifact/config/retry_policies.yaml)

## Skill Output:

**Output Type(s):** [code, configuration, shell commands, guidance]

**Output Format:** [Markdown documentation with Python and shell examples plus YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes retry results, fallback results, degradation reports, and audit log exports when used in code.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
