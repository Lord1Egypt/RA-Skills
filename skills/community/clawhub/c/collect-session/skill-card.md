## Description:

Installs and configures an OpenClaw hook that captures session telemetry and writes Markdown summaries, an index, and JSONL analytics when `/new` or `/reset` is issued.

This skill is ready for commercial/non-commercial use.

## Publisher:

[virtualpaul](https://clawhub.ai/user/virtualpaul)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install a session-collection hook, configure output and LiteLLM settings, run backfills, and troubleshoot capture behavior. It supports searchable session history, cost tracking, and telemetry review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically records broad session telemetry and stores long-term Markdown and JSONL logs.

Mitigation: Keep the output directory out of shared or synced repositories, protect local permissions, and periodically delete or archive generated logs.

Risk: LLM enrichment can send user-message excerpts and a LiteLLM key to a configurable endpoint.

Mitigation: Use `--no-llm` or leave `LITELLM_API_KEY` unset for sensitive work, and set `LITELLM_BASE_URL` only to a trusted local endpoint.

## Reference(s):


## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JavaScript, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The installed collector writes Markdown session reports, a Markdown session index, and a JSONL analytics log.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
