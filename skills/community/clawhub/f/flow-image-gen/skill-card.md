## Description:

Generate the storyboard images for a short-form video job. Walks the image_prompts[] array from a job's input.json, calls Google's Gemini image model to render each prompt as a PNG, and saves files into the job's images/ folder using the filenames specified by the timeline. Up to 4 images in parallel. Use whenever the orchestrator hands off image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pushpendrachauhan](https://clawhub.ai/user/pushpendrachauhan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video-generation agents use this skill to generate storyboard PNGs from a job folder's input.json, mapping image prompts to timeline filenames and keeping output in the job's images directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runner has file-write containment and output validation weaknesses.

Mitigation: Install only if you trust the job directory contents, run in a clean private per-job directory, and avoid preexisting or shared images folders until symlink rejection and expected-PNG validation are added.

Risk: Image prompts are sent to Google's Gemini API using GEMINI_API_KEY.

Mitigation: Do not process sensitive prompts unless sharing them with the Gemini API is acceptable for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pushpendrachauhan/skills/flow-image-gen)
- [Google Gemini image generation endpoint](https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent)

## Skill Output:

**Output Type(s):** [files, text, configuration]

**Output Format:** [PNG image files plus shell status lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes one PNG per image prompt to the job images directory and reports per-image success, skip, or failure status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
