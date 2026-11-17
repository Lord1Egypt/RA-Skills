## Description:

Wire any OpenAI-compatible LLM API into Hermes Agent as a custom provider - Cloudflare Workers AI, self-hosted vLLM, Ollama, LM Studio, or any service that implements /v1/chat/completions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mina-atef-00](https://clawhub.ai/user/mina-atef-00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Hermes Agent for OpenAI-compatible LLM endpoints, including hosted providers and self-hosted services. It helps them validate endpoint compatibility, place credentials correctly, migrate provider settings, and avoid stale model or provider pins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider reconfiguration can route prompts, model traffic, and API costs to a third-party or self-hosted endpoint.

Mitigation: Use only trusted providers, keep API tokens scoped to the intended service, and review the final Hermes configuration before use.

Risk: Credential placement mistakes can expose an API token to the wrong endpoint or leave a non-OpenAI provider without the required key.

Mitigation: Follow the host-gated key guidance and place non-OpenAI credentials in Hermes config entries rather than relying on OPENAI_API_KEY.

Risk: Provider migrations can leave stale auxiliary, delegation, cron, MOA, or profile model pins that continue sending traffic to an old provider.

Mitigation: Back up configs, sweep every LLM consumer, grep for old-provider references, validate YAML, and smoke test the selected provider after migration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mina-atef-00/skills/custom-llm-provider-setup)
- [Publisher profile](https://clawhub.ai/user/mina-atef-00)
- [Project homepage](https://github.com/mina-atef-00/agent-skills)
- [Hermes Providers docs](https://hermes-agent.nousresearch.com/docs/integrations/providers)
- [Cloudflare Workers AI - Hermes Custom Provider](references/cloudflare-workers-ai.md)
- [Cloudflare Workers AI OpenAI compatibility](https://developers.cloudflare.com/workers-ai/configuration/open-ai-compatibility/)
- [Cloudflare Workers AI models](https://developers.cloudflare.com/workers-ai/models/)
- [Provider Migration Sweep](references/provider-migration-sweep.md)
- [Provider Model Identity Tracing](references/provider-model-tracing.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider-specific endpoint URLs, model identifiers, credential placement guidance, validation commands, and migration checklists.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
