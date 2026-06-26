## Description: <br>
Parses Douyin share links and returns watermark-free video download URLs with quota checking and license activation tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuss228](https://clawhub.ai/user/fuss228) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this MCP/CLI skill to extract Douyin video metadata and downloadable no-watermark links, and to check or activate usage quotas for the tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports exposed remote database credentials and direct updates to a payment database from the user-installed package. <br>
Mitigation: Rotate and remove the embedded credentials, and replace direct MySQL activation with a narrow HTTPS backend API before broad deployment. <br>
Risk: The skill performs no-watermark Douyin extraction and uses local quota state plus remote activation behavior. <br>
Mitigation: Install only when the publisher is trusted, use it only where rights and platform terms permit, and review the local state and activation behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fuss228/douyindownload) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [MCP text responses containing JSON or status text, plus Markdown documentation with shell commands and MCP configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include video metadata, cover URLs, downloadable video URLs, quota status, plan status, and activation results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
