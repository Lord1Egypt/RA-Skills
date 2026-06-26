## Description: <br>
Generate and edit images, create videos, produce icons and audio, search stock content, and run AI utilities through Freepik's API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cohnen](https://clawhub.ai/user/cohnen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this OpenClaw skill to have an agent call Freepik's API for media generation, editing, stock search, and related AI utilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent needs access to a Freepik API key and sends prompts, selected media URLs or files, and related request metadata to Freepik. <br>
Mitigation: Install only when Freepik API use is acceptable, scope the FREEPIK_API_KEY appropriately, and avoid submitting sensitive prompts or media. <br>
Risk: Freepik API calls may consume account credits. <br>
Mitigation: Review requested operations before execution and monitor usage in the Freepik developer account. <br>
Risk: Generated media may be retained locally in session output folders. <br>
Mitigation: Review and remove saved outputs under ~/.freepik/sessions/ when local retention is not desired. <br>


## Reference(s): <br>
- [Freepik API Documentation](https://docs.freepik.com) <br>
- [Freepik Developers Dashboard](https://www.freepik.com/developers/dashboard) <br>
- [Freepik OpenClaw Skill Repository](https://github.com/SqaaSSL/freepik-openclaw-skill) <br>
- [Freepik ClawHub Listing](https://clawhub.ai/cohnen/freepik) <br>
- [Models Reference](models-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, API responses, result URLs, and locally saved media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FREEPIK_API_KEY; generated media is saved under ~/.freepik/sessions/ when downloaded.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
