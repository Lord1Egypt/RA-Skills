## Description: <br>
Generate ultra-realistic images and Instagram content using Gemini 2.0 Flash Experimental for photorealistic images, social media content, and visual assets for Instagram workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Vitja1988](https://clawhub.ai/user/Vitja1988) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content operators use this skill to generate local image files and Instagram-ready captions from text prompts using Gemini. It supports standalone photorealistic image generation and paired image-plus-caption workflows for social media preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Instagram workflow references separate posting automation with persistent mode changes and weak approval boundaries. <br>
Mitigation: Review that automation separately and require explicit approval before running any workflow that can post to an Instagram account. <br>
Risk: Gemini prompts and API credentials may expose sensitive information if handled casually. <br>
Mitigation: Use GEMINI_API_KEY or a secret manager instead of command-line key flags, and avoid sending confidential or sensitive prompts to Gemini. <br>
Risk: Generated images and captions may be inaccurate, unsuitable, or misaligned with the intended brand or account. <br>
Mitigation: Review generated files and captions before publishing or handing them to posting tools. <br>


## Reference(s): <br>
- [Gemini API Reference](references/gemini_api.md) <br>
- [Google AI Studio API Key](https://aistudio.google.com/app/apikey) <br>
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs) <br>
- [Gemini API Pricing](https://ai.google.dev/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with Python command examples; generated outputs are image files and caption text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY or an explicitly supplied Gemini API key; generated files are saved locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
