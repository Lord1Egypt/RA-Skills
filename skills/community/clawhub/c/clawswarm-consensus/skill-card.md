## Description:

ClawSwarm runs multiple AI agents with configurable roles, models, and temperatures, then aggregates numeric predictions into a consensus forecast.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alanarchy](https://clawhub.ai/user/alanarchy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use ClawSwarm to orchestrate multiple LLM agents for numeric forecasts and aggregate their predictions into a JSON consensus output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted configs can route prompts or credentials to an unsafe API endpoint.

Mitigation: Run only trusted configs and limit provider/base_url values to official provider URLs or local Ollama.

Risk: Direct api_key values in shared config files can expose credentials.

Mitigation: Prefer api_key_env and keep secrets in environment variables rather than config files.

Risk: Large agent counts or very short delays can create unintended API spend or rate-limit pressure.

Mitigation: Set deliberate agent counts and delay_ms values before running a swarm.

## Reference(s):

- [ClawSwarm Configuration Reference](references/config-reference.md)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML/JSON configuration examples and JSON result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Swarm runs can call configured LLM APIs and return consensus metrics plus individual predictions.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
