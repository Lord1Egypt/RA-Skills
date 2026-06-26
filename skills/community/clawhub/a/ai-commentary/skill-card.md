## Description: <br>
Scenario-focused Sparki skill for commentary-style edits while using the latest official Sparki setup, API-key, and upload workflow guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to turn local video files into commentary-style, narrated, explainer, recap, or reaction edits through Sparki's upload and editing workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected video files and edit prompts are sent to Sparki for processing. <br>
Mitigation: Use the skill only for footage and prompts that are appropriate to share with Sparki. <br>
Risk: Running sparki setup saves the Sparki API key in local OpenClaw configuration. <br>
Mitigation: Prefer SPARKI_API_KEY from the environment when local credential persistence is not desired. <br>
Risk: Downloaded video results are written to a local output path. <br>
Mitigation: Choose the download output directory deliberately and review file locations before sharing or retaining generated videos. <br>


## Reference(s): <br>
- [AI Commentary on ClawHub](https://clawhub.ai/fischerlam/ai-commentary) <br>
- [fischerlam ClawHub Publisher Profile](https://clawhub.ai/user/fischerlam) <br>
- [Sparki](https://sparki.io) <br>
- [Sparki Telegram Upload](https://t.me/Sparki_AI_bot/upload) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands; CLI responses are JSON and downloaded results are video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SPARKI_API_KEY for authentication, sends selected videos to Sparki, and writes downloaded outputs to the configured local output path.] <br>

## Skill Version(s): <br>
1.0.12 (source: SKILL.md frontmatter, _meta.json, and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
