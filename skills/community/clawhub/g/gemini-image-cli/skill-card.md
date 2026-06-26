## Description: <br>
Generate and edit images with a bundled Gemini native image-generation CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pluiez](https://clawhub.ai/user/pluiez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate or edit images through Gemini, choose supported image models and options, inspect raw responses, and troubleshoot provider or request failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected reference images may be sent to Google Gemini or to the configured proxy. <br>
Mitigation: Use --provider local for more sensitive work and keep API keys scoped and private. <br>
Risk: Retries, batches, or --overwrite can cause additional quota use or local file replacement. <br>
Mitigation: Avoid retries, batches, or --overwrite unless the user explicitly intends the extra request volume or replacement. <br>
Risk: A local proxy still grants image-generation capability. <br>
Mitigation: Bind the proxy to 127.0.0.1, avoid arbitrary URL forwarding, and enforce model, request size, rate, and quota limits as needed. <br>


## Reference(s): <br>
- [Gemini Image CLI Behavior](references/behavior.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/pluiez/gemini-image-cli) <br>
- [gemini-balance local proxy](https://github.com/snailyp/gemini-balance) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Machine-readable stdout lines with generated image, raw JSON, and optional text file paths; human-readable logs on stderr.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save image files, raw Gemini response JSON, and optional text output; image extension follows the returned MIME type.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and script VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
