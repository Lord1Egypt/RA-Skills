## Description: <br>
A multi-functional audio generation tool for SFX generation, video-to-audio and text-to-audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yjx-research](https://clawhub.ai/user/yjx-research) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative media users use this skill to generate sound effects or synchronized audio from text prompts, video files, and optional reference audio through the ControlFoley service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, videos, and reference audio are sent to Xiaomi's ControlFoley service for remote processing. <br>
Mitigation: Use non-sensitive media and review the service terms for retention and access policies before processing private or regulated content. <br>
Risk: Generated media is downloaded from remote result URLs and saved locally. <br>
Mitigation: Choose the output directory intentionally and inspect generated files before reuse or redistribution. <br>
Risk: The service does not require an API key, so accidental high-volume use can create unnecessary external load. <br>
Mitigation: Start with small test clips and keep generation counts and repeated submissions deliberate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yjx-research/controlfoley-audio-generator) <br>
- [ControlFoley API Reference](artifact/references/api-reference.md) <br>
- [ControlFoley Service](https://controlfoley.ai.xiaomi.com) <br>
- [ControlFoley Project Page](https://yjx-research.github.io/ControlFoley_web_page/) <br>
- [ControlFoley Model Weights](https://huggingface.co/YJX-Xiaomi/ControlFoley/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands; generated outputs are local FLAC audio and MP4 video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a remote ControlFoley service, polls task status, and saves returned media files to the selected output directory.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
