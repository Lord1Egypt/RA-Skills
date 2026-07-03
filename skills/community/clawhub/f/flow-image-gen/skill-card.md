## Description: <br>
Generate the storyboard images for a short-form video job by walking the image_prompts[] array from a job's input.json, calling Google's Gemini image model to render each prompt as a PNG, and saving files into the job's images/ folder using the filenames specified by the timeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pushpendrachauhan](https://clawhub.ai/user/pushpendrachauhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video-pipeline agents use Flow Image Gen to turn a short-form video job's storyboard prompts into PNG files saved in the job images folder. It supports repeatable job-folder execution with concurrency, retry, and output-size checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts and style details from input.json are sent to Google Gemini using GEMINI_API_KEY. <br>
Mitigation: Use only prompts approved for the relevant Google account and project, and avoid sensitive, proprietary, or regulated content unless that use is approved. <br>
Risk: Image generation can consume paid Gemini API quota and may fail when billing or free-tier limits are exhausted. <br>
Mitigation: Review the number of requested images and project quota before execution, and inspect failed job output before re-running. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pushpendrachauhan/skills/flow-image-gen) <br>
- [Google Gemini Image Generation API Endpoint](https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Text] <br>
**Output Format:** [PNG image files plus stdout and stderr status lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes PNG files to <job>/images/ and supports IMAGE_GEN_PARALLEL concurrency.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
