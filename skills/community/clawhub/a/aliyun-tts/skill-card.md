## Description: <br>
Alibaba Cloud Text-to-Speech synthesis service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guang384](https://clawhub.ai/user/guang384) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to synthesize text into Alibaba Cloud TTS audio files for voice replies or generated speech output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends text to Alibaba Cloud and stores Aliyun credentials for service access. <br>
Mitigation: Use restricted, least-privilege Aliyun credentials and avoid sending sensitive or regulated text unless the deployment has approved controls. <br>
Risk: The security summary reports that the token request uses unencrypted HTTP. <br>
Mitigation: Review or patch the token-request path before production use, and deploy only after confirming the transport meets your security requirements. <br>
Risk: The skill writes generated audio to user-specified output paths. <br>
Mitigation: Choose safe output locations and review generated files before sharing or using them in downstream workflows. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration] <br>
**Output Format:** [Audio file output with command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Aliyun app key and access-key credentials; supports output path, voice, audio format, and sample-rate options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
