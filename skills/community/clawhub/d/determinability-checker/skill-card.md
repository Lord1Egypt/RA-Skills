## Description:

Check target determinability on a bounded finite configuration set.

This skill is ready for commercial/non-commercial use.

## Publisher:

[schchit](https://clawhub.ai/user/schchit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to evaluate whether a target field is determinable from observations across a bounded finite set of configurations, and to obtain counterexamples or evidence suggestions when it is not.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote API exposure may exceed the package's local-service assumptions.

Mitigation: Run the service only on 127.0.0.1 unless it is protected by a trusted proxy with TLS plus request-rate and read-time limits.

Risk: Bearer-token or trusted-key configuration could expose service access if stored in source control or shared outside the service account.

Mitigation: Keep JEP_CLIENTS and trusted-key configuration out of source control, generate strong bearer tokens, and grant only the check permission unless other helpers are intentionally used.

Risk: A determinability result may be mistaken for factual correctness, legal compliance, or execution permission.

Mitigation: Treat can_proceed as a statement about the submitted finite dataset only, and require separate validation before acting on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/schchit/skills/determinability-checker)
- [README](README.md)
- [Security profile](SECURITY.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [JSON API responses with determinability status, decision tables, counterexamples, missing evidence, and guidance messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bounded to 1-128 configurations, at most 32 evidence fields, and finite JSON scalar observation and target values.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
