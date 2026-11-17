## Description:

This skill helps e-commerce, product photography, brand, and live-commerce teams generate or edit Xiaohongshu commerce images through AI-HIVE, with optional reference-image upload, task polling, and result download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, e-commerce operators, product photographers, brand teams, and live-commerce teams use this skill to create Xiaohongshu product images, detail-page visuals, ad creatives, posters, social commerce graphics, retouching outputs, background replacements, and reference-guided image edits. Developers and agents can also use its CLI workflow to configure AI-HIVE access, upload media, submit generation jobs, preserve task IDs, poll task status, and download results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AI-HIVE API key may be sent to a custom base URL if --base-url or AI_HIVE_BASE_URL is set.

Mitigation: Use the default AI-HIVE endpoint unless a custom endpoint is explicitly trusted, and keep API keys scoped and revocable.

Risk: Reference images or other product media can be uploaded to AI-HIVE as part of generation jobs.

Mitigation: Confirm that uploaded media is appropriate for AI-HIVE processing and does not contain private, sensitive, or unauthorized content.

Risk: Image generation tasks may incur charges or duplicate work if jobs are resubmitted after a timeout.

Mitigation: Preserve task IDs, poll existing tasks before resubmitting, and confirm budget before batch or high-cost generation.

Risk: Runtime dependency installation can introduce supply-chain risk.

Mitigation: Install dependencies in a virtual environment and pin reviewed versions where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-xiaohongshu-ecommerce-image-generation-editing)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with bash commands, configuration notes, task IDs, JSON status output, and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI-HIVE API key; generated image formats depend on the active model configuration returned by AI-HIVE.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
