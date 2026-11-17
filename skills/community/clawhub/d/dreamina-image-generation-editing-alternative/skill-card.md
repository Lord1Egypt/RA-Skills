## Description:

This skill helps agents migrate Dreamina or Jimeng-style Chinese image generation and reference-image editing workflows to AI Hive with Nano Banana Pro while preserving prompt intent, subject consistency, reference-image roles, and commercial delivery constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to convert Dreamina or Jimeng-style Chinese image prompts and reference-image editing tasks into AI Hive commands for product, character, ecommerce, and marketing image workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected reference images are sent to AI Hive.

Mitigation: Use this skill only when the user trusts AI Hive and avoid sensitive, confidential, or regulated reference images.

Risk: Remote task responses may cause generated files to be downloaded outside the expected scope or overwrite local files.

Mitigation: Use a dedicated output directory with no important files and review the skill before routine use.

Risk: The security scan recommends stronger controls around remote URLs, filenames, and download size or type.

Mitigation: Patch URL allowlists, filename sanitization, and download size/type limits before deploying this skill in repeated commercial workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/dreamina-image-generation-editing-alternative)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash examples, CLI JSON task responses, and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved to the configured output directory unless task output is requested without download.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
