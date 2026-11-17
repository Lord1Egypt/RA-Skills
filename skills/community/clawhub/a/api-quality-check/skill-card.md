## Description:

Check coding-model API quality, capability fit, and drift with LT-lite and B3IT-lite for OpenAI, OpenAI-compatible, and Anthropic endpoints used by coding CLIs, terminal agents, and OpenClaw-style workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chekhovin](https://clawhub.ai/user/chekhovin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check whether coding-model API endpoints are fit for CLI and agent workflows. It supports smoke checks, first-token detection, logprob tracking, baseline creation, and drift detection for OpenAI, OpenAI-compatible, and Anthropic-style endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider configs, generated outputs, logs, or transcripts can expose plaintext API keys.

Mitigation: Keep provider configs and generated output directories private, avoid publishing report folders as CI artifacts or static pages, avoid commands that print keys into logged stdout, and rotate any keys already copied into shared reports or transcripts.

Risk: Unsupported endpoint capabilities can make LT-lite or B3IT-lite checks unsuitable for a target API.

Mitigation: Run the smoke check first, use LT-lite only when logprobs are present, use B3IT-lite only when first-token text is usable, and review generated JSON or HTML reports before acting on drift results.

## Reference(s):

- [Config Schema](references/config-schema.md)
- [Endpoint Types Playbook](references/endpoint-types-playbook.md)
- [Kimi Anthropic Quickstart](references/kimi-anthropic-quickstart.md)
- [Kimi Coding Quickstart](references/kimi-coding-quickstart.md)
- [Example Provider List](references/providers.example.json)
- [Workflow Notes](references/workflows.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with bash examples, plus generated JSON and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [File-based outputs include provider configs, smoke results, baselines, drift reports, and optional HTML summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
