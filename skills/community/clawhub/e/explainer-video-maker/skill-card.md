## Description: <br>
Create narrated explainer and tutorial videos by relaying a user's topic and optional media to Pexo, which writes the script, generates visuals, adds TTS voiceover and captions, and returns the finished video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pexo](https://clawhub.ai/user/pexo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn product, concept, or process explanations into narrated videos through Pexo's hosted video agent. It supports project creation, optional media upload, polling, revision requests, and delivery of the final video URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and uploaded media are sent to Pexo's hosted service. <br>
Mitigation: Do not upload confidential prompts, images, audio, or videos unless Pexo's handling of that data is acceptable for the use case. <br>
Risk: The skill requires a Pexo API key stored in ~/.pexo/config or environment variables. <br>
Mitigation: Treat the config as a secret, restrict file permissions, avoid committing or sharing it, and rotate the key if exposure is suspected. <br>
Risk: Video generation can consume credits and may direct users to purchase more credits. <br>
Mitigation: Require explicit user action for credit purchases and use Pexo's billing pages rather than making purchases silently. <br>


## Reference(s): <br>
- [Pexo](https://pexo.ai) <br>
- [Explainer Video Maker on ClawHub](https://clawhub.ai/pexo/explainer-video-maker) <br>
- [Setup Checklist](references/SETUP-CHECKLIST.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with shell commands, JSON script outputs, project links, and final asset URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Pexo project IDs and asset IDs; final delivery includes a full signed asset URL and project link.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
