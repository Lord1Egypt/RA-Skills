## Description:

Uses AI-HIVE to generate and edit GPT Image 2 commercial images from prompts and reference images, including text layout, localized edits, product-detail visuals, task polling, and result downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to create or edit commercial GPT Image 2 visuals for brand design, ecommerce listings, advertising, social channels, and product-detail assets through AI-HIVE.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI-HIVE API credentials and can send the bearer key to a configured endpoint.

Mitigation: Use only the official AI-HIVE endpoint unless the destination is fully trusted, store the key in a dedicated low-privilege account when possible, and rotate the key if it may have been used with a custom or untrusted endpoint.

Risk: The security verdict is suspicious even though no individual risk findings were reported.

Mitigation: Review before installing, install dependencies in an isolated virtual environment, and scan the artifact before deployment.

## Reference(s):

- [AI-HIVE product entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-gpt-image-2-image-generation-editing)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, files]

**Output Format:** [Markdown guidance with bash commands, JSON task responses, and downloaded image files from the CLI when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI-HIVE API key; generation commands return task IDs and can poll for downloadable results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
