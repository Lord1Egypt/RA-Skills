## Description: <br>
Generates and publishes novels to fireseed.online by authenticating, creating a novel, posting chapters, and optionally uploading a cover through HTTP APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanzhishuyuan](https://clawhub.ai/user/sanzhishuyuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agent users use this skill to generate multi-chapter novels and publish them to the FireSeed platform through API calls, including account authentication, chapter publishing, and optional cover upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect FireSeed credentials or tokens and store a token locally. <br>
Mitigation: Use a pre-created limited token where possible, avoid entering raw account passwords in chat, and remove stored tokens when the skill is no longer needed. <br>
Risk: Trigger phrases can cause automatic publishing actions on an external platform with limited user control. <br>
Mitigation: Install only in agent profiles where automatic FireSeed publishing is intended, and review or disable auto-invocation triggers before deployment. <br>
Risk: Generated chapters may be published publicly before human review. <br>
Mitigation: Review generated chapter text and cover content before allowing publication in workflows that require editorial or compliance approval. <br>


## Reference(s): <br>
- [FireSeed platform](https://fireseed.online) <br>
- [API reference](references/api-guide.md) <br>
- [Novel template](resources/novel-template.md) <br>
- [ClawHub skill listing](https://clawhub.ai/sanzhishuyuan/fireseed-novel-auto-publish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration] <br>
**Output Format:** [Markdown and JSON HTTP request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish generated novel content to an external public platform and may store an authentication token locally.] <br>

## Skill Version(s): <br>
3.5.1 (source: evidence.release.version, SKILL.md frontmatter, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
