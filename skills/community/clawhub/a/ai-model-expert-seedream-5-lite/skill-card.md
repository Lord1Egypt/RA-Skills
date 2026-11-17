## Description:

Generates and edits Seedream 5.0 Lite images through AI-HIVE, including text-to-image, reference-guided image generation, task polling, and result downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, e-commerce operators, marketing teams, brand teams, and content creators use this skill to create product images, advertising visuals, posters, social media assets, retouching outputs, background replacements, and consistent-character imagery through AI-HIVE.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be sent to an arbitrary configured server if the API base URL is changed.

Mitigation: Use only the official AI-HIVE endpoint unless using a separate disposable key; avoid --base-url, AI_HIVE_BASE_URL, or config base_url overrides.

Risk: Prompts and reference media are uploaded for remote processing.

Mitigation: Use the skill only when comfortable sending those inputs to AI-HIVE, and confirm rights to any reference material before submission.

Risk: Batch generation can create cost exposure or duplicate charge risk if jobs are resubmitted after timeouts.

Mitigation: Confirm costs before batch jobs, keep the returned taskId, and query the existing task instead of resubmitting timed-out work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-model-expert-seedream-5-lite)
- [AI-HIVE Entry Point](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON task responses, and downloaded image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is saved to the configured output directory; task IDs can be retained and queried later.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
