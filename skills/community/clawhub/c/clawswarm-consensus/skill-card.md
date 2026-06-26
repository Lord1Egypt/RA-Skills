## Description: <br>
ClawSwarm runs multiple LLM prediction agents with configurable roles and temperatures, then aggregates their numeric forecasts with statistical consensus methods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alanarchy](https://clawhub.ai/user/alanarchy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to run configurable groups of LLM agents for price, value, or outcome prediction and combine the individual predictions into a single consensus forecast. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured target data, context, role prompts, and API authorization may be sent to the selected LLM provider. <br>
Mitigation: Use approved providers for sensitive data, avoid regulated or proprietary context unless authorized, and review provider, model, and base_url settings before execution. <br>
Risk: API keys can be exposed if placed directly in configuration files. <br>
Mitigation: Use api_key_env and environment variables instead of storing secrets in YAML or JSON config files. <br>
Risk: Large agent counts can increase provider cost and rate-limit exposure. <br>
Mitigation: Start with --dry-run or small agent counts, configure delay_ms, and scale only after confirming expected behavior and cost. <br>
Risk: Consensus forecasts can be wrong or misleading for high-stakes decisions. <br>
Mitigation: Treat outputs as decision support, review individual predictions and filtering details, and apply domain-specific validation before acting. <br>


## Reference(s): <br>
- [Configuration Reference](references/config-reference.md) <br>
- [ClawHub Release Page](https://clawhub.ai/alanarchy/clawswarm-consensus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with configuration examples, shell commands, and JSON prediction output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The swarm runner can call configured LLM providers and the consensus engine emits fields such as final_price, confidence, bull_ratio, participant_count, and filtering details.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
