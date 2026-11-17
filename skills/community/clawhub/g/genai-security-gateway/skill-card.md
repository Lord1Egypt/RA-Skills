## Description:

Local-first LLM prompt firewall for MCP tools, AI agents, and gateways that audits prompts for prompt injection, jailbreak attempts, developer-mode bypasses, hidden-system-prompt extraction, and API key leakage before tool use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[margaretzybgl](https://clawhub.ai/user/margaretzybgl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill as a repeatable preflight check before user prompts reach MCP tools, shells, browsers, code interpreters, retrieval, or downstream model gateways. It returns structured PASS or BLOCK decisions with detector, risk level, reason, suggested action, and optional semantic similarity details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-privilege agent deployments may over-rely on this scanner as a complete security boundary.

Mitigation: Use it as one preflight layer alongside MCP and tool allowlists, provider safety settings, output filtering, rate limits, abuse monitoring, and human review for high-risk workflows.

Risk: Runtime dependencies and the first semantic model run may introduce supply-chain review needs or network-dependent behavior.

Mitigation: Install in a virtual environment or container, pin and review dependencies, and cache or vendor the sentence-transformer model when offline or controlled deployment behavior matters.

Risk: Prompts or secrets may be exposed through wrapper, terminal, or application logs around the scanner.

Mitigation: Avoid logging raw prompts and secrets; store only coarse fields such as suggested_action, detector, and risk_level when audit logging is needed.

Risk: Static and semantic detection can produce false positives or false negatives.

Mitigation: Tune the semantic threshold and template set for the deployment context, and keep human review in the loop for sensitive decisions.

## Reference(s):

- [Security Policy](artifact/references/security-policy.md)
- [Jailbreak Templates](artifact/references/jailbreak_templates.json)
- [Test Prompts](artifact/references/test_prompts.json)
- [ClawHub Skill Page](https://clawhub.ai/margaretzybgl/skills/genai-security-gateway)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Shell commands]

**Output Format:** [JSON audit results with Markdown and inline bash examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured decisions include is_safe, risk_level, reason, suggested_action, detector, semantic_score, semantic_threshold, semantic_timeout_seconds, and matched_template.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
