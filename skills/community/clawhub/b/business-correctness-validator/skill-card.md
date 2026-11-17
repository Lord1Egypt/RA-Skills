## Description:

Validates generated business content against platform rules and returns JSON pass, warning, or blocked results; broader price and risk-metric claims should be verified in the target environment before production reliance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill as a post-generation validation gate before publishing generated marketing or product content. Production users should confirm the required MCP servers, business-rule configuration, and any blocking paths in their own environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact describes price validation, risk-metric enforcement, blocking, and alerting paths that may not be fully implemented.

Mitigation: Verify and test those paths in the deployment environment before relying on the skill as a production gate.

Risk: Violation logs may contain sensitive tenant or business data.

Mitigation: Store logs with appropriate access controls, retention limits, and handling procedures for tenant data.

Risk: The skill depends on configured MCP servers and BUSINESS_RULES_CONFIG for environment-specific behavior.

Mitigation: Confirm required MCP configuration and business-rule files before enabling automated blocking or alerting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/business-correctness-validator)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON result examples and shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Validation results use success, result, risk_level, violations, error, and code fields.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
