## Description: <br>
Transforms a foreign tourist's identity into Chinese name options, classical poetry, cultural explanations, and traditional Chinese art prompts or image outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoaipensieve](https://clawhub.ai/user/xiaoaipensieve) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel or culture-focused agents use this skill to create a Chinese cultural identity package from a user's name, theme preferences, and optional gender preference. The package can include Chinese name options, Jueju or Lushi poetry, translations, cultural notes, seal carving prompts, Shanshui landscape prompts, and ancient portrait avatar prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles personal identity details such as a user's name, theme preferences, and optional gender preference. <br>
Mitigation: Use it only for explicit Chinese naming or art requests, and avoid sharing sensitive personal details beyond what is needed for the requested output. <br>
Risk: Session memory and telemetry are not scoped clearly in the security evidence. <br>
Mitigation: Review whether analytics or memory can be disabled or documented before deployment, and clear stored session details when they are no longer needed. <br>
Risk: Broad trigger phrases could activate the skill outside a clear cultural naming or art workflow. <br>
Mitigation: Tighten trigger phrases and confirm user intent before collecting identity details or generating images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoaipensieve/cultural-naming-art) <br>
- [Tencent SkillHub listing](https://skilhub.cloud.tencent.com/skills/cultural-naming-art) <br>
- [Deployment guide](artifact/DEPLOYMENT_GUIDE.md) <br>
- [Tencent SkillHub manifest](artifact/tencent_skilhub_manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Image generation prompts, Configuration] <br>
**Output Format:** [Markdown-style conversational text with structured name, poem, translation, cultural-note, and image-prompt sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request a name, theme preferences, and optional gender preference; may use session memory for selected names, poems, and art choices.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
