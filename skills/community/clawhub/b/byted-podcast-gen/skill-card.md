## Description: <br>
将某个话题或者网页内容总结合成为播客音频（Podcast）。基于火山引擎豆包语音播客合成协议生成最终音频。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to turn a short topic, webpage, downloadable document, uploaded document, or long text into podcast-style speech audio with a segmented transcript. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Podcast inputs, webpage URLs, document contents, and generated audio are handled by the Bytedance/Volcengine speech service. <br>
Mitigation: Avoid confidential or regulated inputs unless the provider terms, retention expectations, and account controls are acceptable. <br>
Risk: Credential provisioning and persistence are under-disclosed, and the skill may store a speech API key in scripts/.env. <br>
Mitigation: Use a dedicated low-privilege API key, rotate it regularly, and check or remove scripts/.env after use. <br>


## Reference(s): <br>
- [Volcengine Doubao Podcast product documentation](https://www.volcengine.com/docs/6561/1668014?lang=zh) <br>


## Skill Output: <br>
**Output Type(s):** [Audio, JSON, Files] <br>
**Output Format:** [JSON status object with a local audio path, optional service-provided audio URL, task identifier, and segmented transcript; generated audio file in MP3, WAV, or OGG format.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Volcengine/Bytedance speech service credentials. Audio URLs may be time-limited, and source text or URLs are processed by the external speech service.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
