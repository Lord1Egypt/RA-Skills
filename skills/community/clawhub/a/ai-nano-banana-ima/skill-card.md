## Description:

Nano Banana-only image generation on IMA Open API supporting text-to-image and image-to-image workflows with budget and premium model choices, deterministic size and aspect-ratio handling, and an IMA_API_KEY runtime requirement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allenfancy-gan](https://clawhub.ai/user/allenfancy-gan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate or edit images through IMA Open API using the Nano Banana model family. It helps agents choose supported task types, models, sizes, aspect ratios, and script parameters for prompt-only or reference-image workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and local image paths may be retained in local logs during failures or normal operation.

Mitigation: Avoid confidential prompts and private image paths, review local logs before sharing the machine, and periodically delete ~/.openclaw/logs/ima_skills/.

Risk: The IMA API key and image inputs are sent to documented IMA services for generation and local-image upload workflows.

Mitigation: Use a scoped or test API key for initial testing, avoid sensitive image uploads unless this data flow is acceptable, and rotate the key if exposure is suspected.

Risk: User model preferences persist locally until removed.

Mitigation: Delete ~/.openclaw/memory/ima_prefs.json when retained model preferences are no longer desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allenfancy-gan/skills/ai-nano-banana-ima)
- [Publisher profile](https://clawhub.ai/user/allenfancy-gan)
- [IMA Studio](https://imastudio.com/)
- [IMA API key page](https://www.imaclaw.ai/imaclaw/apikey)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command templates and JSON result objects from the bundled image-generation script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return image URLs or rendered media metadata including model, task id, credit use, and elapsed generation information.]

## Skill Version(s):

1.0.9 (source: server release evidence; artifact files report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
