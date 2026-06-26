## Description: <br>
Track AI agent API calls, analyze token usage, and optimize costs for OpenAI, Anthropic, Google, DeepSeek, and other LLM APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Agent Lens to instrument AI API calls, inspect token, cost, latency, and error data, and generate local cost reports. It supports workflows for LLM spend monitoring, prompt cost optimization, and troubleshooting API usage across supported providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records API usage metadata in a local SQLite database. <br>
Mitigation: Review what metadata will be collected, keep sensitive workloads under local data-handling controls, and periodically clean or export the database according to retention needs. <br>
Risk: The quick-start flow installs package code from an upstream GitHub repository. <br>
Mitigation: Review the upstream package and pin a trusted revision before using it with sensitive or production workloads. <br>
Risk: Cost estimates use list prices and may differ from actual provider billing after discounts, caching, or account-specific pricing. <br>
Mitigation: Treat reports as estimates and reconcile important decisions against provider billing data. <br>


## Reference(s): <br>
- [Agent Lens ClawHub Skill Page](https://clawhub.ai/lrg913427-dot/agent-lens-tracker) <br>
- [Agent Lens Upstream Repository](https://github.com/lrg913427-dot/agent-lens.git) <br>
- [Publisher Profile](https://clawhub.ai/user/lrg913427-dot) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI command suggestions, instrumentation patterns, cost optimization steps, and local SQLite storage notes.] <br>

## Skill Version(s): <br>
2.15.0 (source: ClawHub release metadata; artifact frontmatter lists 2.14.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
