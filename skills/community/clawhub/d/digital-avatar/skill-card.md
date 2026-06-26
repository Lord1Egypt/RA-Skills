## Description: <br>
Creates digital avatars, optional cloned voices, and talking-head video outputs using providers such as Kling, Jimeng, HeyGen, D-ID, and Synthesia. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OliviaPp8](https://clawhub.ai/user/OliviaPp8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to guide an agent through creating digital avatar assets and rendered talking-head videos from authorized photos, descriptions, scripts, audio, or cloned voices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Avatar generation may send selected photos, voice samples, scripts, and related metadata to third-party avatar providers. <br>
Mitigation: Use only media you are authorized to use, review each provider's privacy and commercial terms, and avoid submitting sensitive material unless the provider is approved for that use. <br>
Risk: Provider API keys and avatar credentials can expose paid accounts or generated assets if committed to project files. <br>
Mitigation: Store credentials in local secret handling or managed secret stores, rotate keys if exposed, and keep generated avatar IDs scoped to the intended provider. <br>


## Reference(s): <br>
- [Backend Setup Guide](references/backend-setup.md) <br>
- [Kling AI](https://klingai.kuaishou.com/) <br>
- [Jimeng Documentation](https://www.volcengine.com/docs/jimeng/) <br>
- [HeyGen API Reference](https://docs.heygen.com/reference/) <br>
- [D-ID API Reference](https://docs.d-id.com/reference/) <br>
- [Synthesia API Reference](https://docs.synthesia.io/reference/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs describe avatar IDs, preview URLs, optional voice IDs, video URLs, duration, and render status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
