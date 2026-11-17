## Description:

AI-HIVE image generation and editing skill for Amazon ecommerce teams that turns prompts and optional reference images into product, listing, advertising, social, and marketing visuals while submitting, polling, and downloading generation results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, product photography teams, brand marketers, designers, and cross-border commerce teams use this skill to create and edit Amazon listing images, product detail visuals, ad creatives, posters, and social commerce images through AI-HIVE. Developers and agents can also use it to initialize credentials, upload reference media, submit image-generation tasks, poll task status, and download generated outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys are used for paid AI-HIVE requests and may be stored under ~/.ai-hive/config.json.

Mitigation: Use environment variables or the initialized config file with restrictive permissions, and do not paste real API keys into public skill files, screenshots, or chats.

Risk: The skill allows endpoint overrides through --base-url and AI_HIVE_BASE_URL, which can redirect API-key-bearing requests.

Mitigation: Use only the official AI-HIVE endpoint unless the alternate endpoint is fully trusted and controlled.

Risk: Reference images and other local media are uploaded to AI-HIVE/object storage before generation.

Mitigation: Do not upload sensitive local files, and confirm that reference media is approved for the intended commercial use.

Risk: Image-generation tasks may incur costs, and repeated submissions after timeouts can duplicate paid work.

Mitigation: Review the runtime pricing snapshot before batch jobs, preserve taskId values, and poll the original task before resubmitting.

Risk: Generated ecommerce visuals can contain inaccurate product facts, unauthorized marks, misleading claims, or unsuitable edits.

Mitigation: Human-review product structure, claims, trademarks, text, dimensions, and channel requirements before publishing.

## Reference(s):

- [AI-HIVE Chat and API Access](https://ai-hive.iclip.cn/chat)
- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-model-expert-amazon-ecommerce-image-generation-editing)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, JSON, Guidance]

**Output Format:** [Markdown guidance with inline bash commands; task commands may print JSON metadata and download generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI-HIVE task IDs; downloads results to ~/Downloads/AiHive by default unless --no-download or --output-dir is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
