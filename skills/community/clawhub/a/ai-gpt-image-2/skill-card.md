## Description:

视觉质量诊断助手适合市场营销、运营、内容媒体、电商在用户提出“这张图够发布吗”这类问题，需要快速拆解目标、判断重点并形成可执行结果时使用，帮助基于输入材料生成摘要、诊断结论、行动建议和可复用交付物。

This skill is ready for commercial/non-commercial use.

## Publisher:

[allinherog-star](https://clawhub.ai/user/allinherog-star)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, operations, media, ecommerce, software, and education users can use this skill to assess whether image materials are ready to publish and to turn image goals, audience context, references, prompts, product notes, and brand requirements into summaries, diagnostic conclusions, action recommendations, and reusable deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runner sends API-key-authenticated requests, prompts, uploaded or referenced image materials, brand requirements, and profile context to an external service.

Mitigation: Install only when the publisher and ai-skills.ai are trusted for that data, avoid submitting sensitive or unlicensed material, and inform users that processing is remote.

Risk: AISKILLS_BASE_URL can redirect execution to a different endpoint.

Mitigation: Review or remove AISKILLS_BASE_URL overrides before use and prefer the default ai-skills.ai endpoint unless an approved endpoint is required.

Risk: The skill requires an API key for remote execution.

Mitigation: Use a limited-scope API key, store it securely, rotate it if exposed, and avoid sharing it in prompts, logs, or generated artifacts.

Risk: The release evidence notes unclear diagnostic-versus-generation purpose and invocation scope.

Mitigation: Review outputs before publication and confirm that the generated guidance matches the intended image-quality review or image-generation workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allinherog-star/skills/ai-gpt-image-2)
- [form-schema.json](artifact/references/form-schema.json)
- [skill.json](artifact/references/skill.json)
- [AI Skills](https://ai-skills.ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [JSON response envelope containing human-facing summaries, diagnostic items, action recommendations, and reusable artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JSON parameters and AISKILLS_API_KEY; may use text prompts, uploaded image references, public reference links, audience, goal, and brand requirement fields.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
