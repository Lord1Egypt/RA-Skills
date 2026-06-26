## Description: <br>
Generates artistic name, signature, and text images by using Baidu AI Studio's ERNIE-Image API with preset calligraphy, cartoon, neon, metallic, and custom styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whisky-12](https://clawhub.ai/user/whisky-12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn names or short text into local artistic signature images, with optional guidance for style selection and credential setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated names, text, and prompt details are sent to Baidu's ERNIE-Image service. <br>
Mitigation: Use the skill only with text and prompts that are acceptable to share with Baidu. <br>
Risk: --set-token stores the Baidu AI Studio access token in plaintext config.json in the skill directory. <br>
Mitigation: Prefer an environment variable or one-time --token on shared, backed-up, or source-controlled machines, and do not commit config.json. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/whisky-12/ernie-image-art-name) <br>
- [Baidu AI Studio Access Token](https://aistudio.baidu.com/account/accessToken) <br>
- [Baidu AI Studio ERNIE-Image API](https://aistudio.baidu.com/llm/lmapi/v3/images/generations) <br>
- [API Docs](references/api_docs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; the script saves generated PNG image files locally.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Baidu AI Studio access token and sends the requested text and prompt to Baidu's ERNIE-Image service.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
