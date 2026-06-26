## Description: <br>
Generate/edit images with Nano Banana Pro (Gemini 3 Pro Image). Supports text-to-image, edits, and 1K/2K/4K resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate new images or edit existing images through a Gemini-compatible Nano Banana Pro image API, with selectable 1K, 2K, or 4K resolution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected input images, and API keys are sent to an external Gemini-compatible image provider. <br>
Mitigation: Use this skill only with provider terms that allow the intended data, avoid confidential prompts or images unless approved, and store API keys in scoped environment or secret storage. <br>
Risk: Generation or editing can fail when the API key is missing, unauthorized, or quota-limited. <br>
Mitigation: Verify GEMINI_API_KEY or --api-key before use and handle provider permission, quota, or 403-style errors before relying on output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cs995279497-byte/chen-nano-banana-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated PNG image files saved to disk] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Gemini-compatible API key via --api-key or GEMINI_API_KEY; supports text-to-image, image editing, and 1K/2K/4K output resolution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
