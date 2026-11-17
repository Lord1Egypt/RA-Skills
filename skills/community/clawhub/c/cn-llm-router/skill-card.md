## Description:

Routes text and multimodal tasks across Chinese language-model providers and helps compare usage and costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fyniujin](https://clawhub.ai/user/fyniujin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can select and call Chinese language models for chat, document, image, embedding, and reranking tasks, while comparing estimated costs and usage across providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, documents, embeddings, and rerank inputs may be sent to configured model providers despite inconsistent privacy documentation.

Mitigation: Use only providers you trust and avoid sending secrets or sensitive content without approval.

Risk: Prompts and related session data may persist in local storage; cached answers may be stale or mismatched.

Mitigation: Use --no-cache for sensitive or critical prompts and clear ~/.cn_llm_router data when needed.

Risk: The legacy ERNIE AK/SK authentication path requires handling additional credentials.

Mitigation: Prefer ERNIE_OPENAI_KEY over the legacy ERNIE AK/SK path.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/fyniujin/skills/cn-llm-router)
- [Routing rules](artifact/references/routing-rules.md)
- [Model registry](artifact/references/models.yaml)
- [Price history](artifact/references/price_history.yaml)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain text or JSON; optional HTML cost reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model recommendations, responses, usage and cost estimates, embeddings, or reranked results.]

## Skill Version(s):

2.7.0 (source: ClawHub release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
