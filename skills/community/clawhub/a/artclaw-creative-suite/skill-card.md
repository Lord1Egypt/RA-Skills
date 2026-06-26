## Description: <br>
Invoke ARTCLAW platform's AI content creation capabilities via REST API for image generation, video generation, workflow execution, multimodal analysis, and job management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alanhuangyoo](https://clawhub.ai/user/alanhuangyoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to submit AI creative generation, workflow, and multimodal analysis jobs to ARTCLAW through a Python CLI and REST API bridge. The skill returns command guidance, JSON job metadata, result URLs, and platform-specific delivery instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The self-update command can overwrite the installed skill from an unpinned GitHub branch without integrity verification. <br>
Mitigation: Avoid self-update unless upstream changes have been reviewed; prefer a reviewed release or pinned package source. <br>
Risk: Prompts, media, and generated outputs may be shared with ARTCLAW and, when delivery is used, with Feishu or Telegram. <br>
Mitigation: Confirm user intent before external delivery and avoid sending sensitive prompts, files, or generated media to third-party services. <br>
Risk: The skill requires sensitive credentials such as ARTCLAW_API_KEY and optional chat delivery tokens. <br>
Mitigation: Store credentials in environment variables or platform credential stores, and do not include secrets in prompts, logs, or command arguments. <br>
Risk: Local ARTCLAW configuration and history may retain job metadata, prompts, or generated asset references. <br>
Mitigation: Review and clean ~/.artclaw history when working with sensitive creative assets or private prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alanhuangyoo/artclaw-creative-suite) <br>
- [ARTCLAW API base](https://artclaw.com/api/v1) <br>
- [ARTCLAW account settings](https://artclaw.com/settings) <br>
- [ARTCLAW platform](https://artclaw.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ARTCLAW job IDs, result URLs, local history paths, and platform-specific delivery metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
