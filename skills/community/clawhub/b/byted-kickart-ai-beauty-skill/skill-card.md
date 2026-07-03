## Description: <br>
Analyzes JPG or PNG portrait images from local files, image URLs, multiple URLs, or archives and returns AI-beautified image links or batch result archives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to apply Volcengine Kickart AI beauty processing to portrait images supplied as local files, URLs, comma-separated URL batches, or compressed archives. It returns processed image URLs for single images and JSON plus ZIP paths for batch processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for cloud access keys or API tokens and security evidence notes that authorization data may be written to local logs. <br>
Mitigation: Use scoped, revocable credentials from a secure secret store, avoid pasting secrets into chat, and review or clear local logs after use. <br>
Risk: Images, image URLs, and archive contents are sent to a remote service for processing. <br>
Mitigation: Do not process sensitive or regulated images unless the remote service terms and data handling are acceptable for the use case. <br>
Risk: Security evidence notes an account or package registration step without clear user consent. <br>
Mitigation: Require explicit user approval before package checks or registration and use an account with the minimum required permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-kickart-ai-beauty-skill) <br>
- [Volcengine Kickart package page](https://console.volcengine.com/kickart/fusion/setting/combobuy?tab=combo) <br>
- [Volcengine IAM access key management](https://console.volcengine.com/iam/keymanage) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [JSON file plus concise text containing signed image URLs or local ZIP paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-image runs return an image result URL; batch URL or archive runs return per-image results and a ZIP path.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter declares 1.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
