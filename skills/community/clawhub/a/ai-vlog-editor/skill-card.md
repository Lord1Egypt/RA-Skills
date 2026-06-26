## Description: <br>
Scenario-focused Sparki skill for editing vlog-style videos while using the latest official Sparki setup, API-key, and upload workflow guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to turn raw daily-life, travel, and lifestyle footage into cleaner vlog-style edits with prompts and Sparki upload/run guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a Sparki API key locally and uses it for remote cloud video editing workflows. <br>
Mitigation: Use a dedicated Sparki API key with limited value when possible, avoid syncing the config directory to backups or dotfiles, and rotate the key if exposed. <br>
Risk: The skill sends videos and reference media to Sparki's cloud service. <br>
Mitigation: Install only when users are comfortable uploading those media assets to Sparki and avoid using sensitive footage without appropriate approval. <br>
Risk: The workflow can download remote media and write to local output paths. <br>
Mitigation: Choose output paths deliberately, review files before bulk workflows, and confirm before deleting uploaded assets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fischerlam/ai-vlog-editor) <br>
- [Sparki homepage](https://sparki.io) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; Sparki CLI commands return JSON and may download video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SPARKI_API_KEY for authenticated Sparki cloud workflows.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
