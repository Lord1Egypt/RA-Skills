## Description: <br>
Use when users mention AI model names, versions, pricing, API IDs, model comparisons, current model availability, or code that references specific AI model IDs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[futurizerush](https://clawhub.ai/user/futurizerush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to reduce stale or hallucinated AI model references by checking model IDs, pricing, deprecation status, API examples, and provider-specific reference notes before writing guidance or code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model names, pricing, deprecation dates, and API identifiers can become stale quickly. <br>
Mitigation: Follow the skill's staleness check and verify current provider documentation before using the reference for code, purchasing, or deployment decisions. <br>
Risk: The artifact includes API quick-start examples that use provider API keys. <br>
Mitigation: Use least-privileged keys, avoid exposing credentials in logs or shared prompts, and test commands in a controlled environment. <br>
Risk: The security review classifies the release as clean but notes it should be used as a reference guide. <br>
Mitigation: Review and scan the skill before deployment, and run only the specific shell or network checks needed for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/futurizerush/ai-common-sense) <br>
- [OpenAI models documentation](https://platform.openai.com/docs/models) <br>
- [OpenAI pricing](https://openai.com/pricing) <br>
- [Anthropic models documentation](https://docs.anthropic.com/en/docs/about-claude/models) <br>
- [Anthropic pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) <br>
- [Google Gemini models documentation](https://ai.google.dev/gemini-api/docs/models) <br>
- [Google Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing) <br>
- [Mistral model documentation](https://docs.mistral.ai/getting-started/models) <br>
- [Mistral pricing](https://mistral.ai/pricing) <br>
- [Meta Llama 4 announcement](https://ai.meta.com/blog/llama-4-multimodal-intelligence/) <br>
- [Cohere pricing](https://cohere.com/pricing) <br>
- [Cohere changelog](https://docs.cohere.com/changelog) <br>
- [DeepSeek](https://deepseek.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown reference guidance with tables, API identifiers, curl examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes last-verified dates and instructs agents to re-check current provider documentation when the reference is stale.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
