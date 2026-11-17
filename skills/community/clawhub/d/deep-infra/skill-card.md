## Description:

Configure DeepInfra model routing with provider auth, model selection, fallback chains, and cost-aware defaults for stable open-source and frontier model workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ats3v](https://clawhub.ai/user/ats3v)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect OpenAI-compatible workflows to DeepInfra, choose task-appropriate models, configure fallback routing, and control cost drift over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real DeepInfra API key could be exposed if pasted into command-line arguments or logs.

Mitigation: Use an environment variable or secret store for DEEPINFRA_API_KEY, avoid command-line key arguments, and do not save keys in memory files or chat.

Risk: Prompt content and selected model metadata leave the local machine when routed inference is requested.

Mitigation: Use the skill only for data appropriate to send to DeepInfra, and remove sensitive content before making inference requests.

Risk: Local routing notes under ~/deep-infra/ may retain operational context that should not include secrets.

Mitigation: Record decisions, pass/fail checks, budgets, and incident summaries only; do not store plaintext credentials or sensitive prompt data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ats3v/skills/deep-infra)
- [DeepInfra OpenAI-compatible model catalog endpoint](https://api.deepinfra.com/v1/openai/models)
- [DeepInfra OpenAI-compatible chat completions endpoint](https://api.deepinfra.com/v1/openai/chat/completions)
- [DeepInfra dashboard](https://deepinfra.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce routing notes for local files under ~/deep-infra/ and DeepInfra API request patterns; requires DEEPINFRA_API_KEY, curl, and jq.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
