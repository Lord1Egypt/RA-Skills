## Description: <br>
Transforms everyday scenes, actions, or subjects into fantastical, magical, ritual-rich vertical videos using WeryAI Seedance 2.0. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to turn a short text brief or one public HTTPS reference image into a fantasy-styled video clip. It guides prompt expansion, parameter confirmation, WeryAI submission, polling, and return of playable video links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generation uses a paid WeryAI API key and each submitted wait run may consume credits. <br>
Mitigation: Install only when the WeryAI integration is trusted, keep WERYAI_API_KEY secret, and review the confirmation before submitting a paid generation task. <br>
Risk: Prompts and image URLs are sent to WeryAI, and the skill requires public HTTPS image URLs. <br>
Mitigation: Avoid confidential prompt text and private or sensitive image URLs; use only public HTTPS images intended for third-party processing. <br>
Risk: The bundled CLI is broader than this specific skill and the script does not enforce the package's allowed model in code. <br>
Mitigation: Before execution, verify that the confirmation and JSON request use model SEEDANCE_2_0 and the allowed duration, aspect ratio, resolution, and audio fields. <br>


## Reference(s): <br>
- [WeryAI Video API Reference](resources/WERYAI_VIDEO_API.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zoucdr/fantasy-transform-video-gen-seedance2-0) <br>
- [Publisher Profile](https://clawhub.ai/user/zoucdr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance and confirmation text, shell command invocation, and JSON task or video URL results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns playable video links when generation succeeds; requires WERYAI_API_KEY, Node.js 18+, network access, and paid WeryAI usage.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
