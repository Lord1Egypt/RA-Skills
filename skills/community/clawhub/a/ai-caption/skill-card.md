## Description: <br>
Scenario-focused Sparki skill for caption-heavy edits while using the latest official Sparki setup, API-key, and upload workflow guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to route caption-first video editing requests through Sparki, including subtitle-heavy shorts and spoken videos intended to remain readable on mute. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-selected videos to Sparki for processing. <br>
Mitigation: Install only if Sparki is trusted with the videos being processed, and request local or manual video tools when uploads are not acceptable. <br>
Risk: The Sparki API key can be saved in the local OpenClaw configuration. <br>
Mitigation: Prefer SPARKI_API_KEY where possible, protect saved keys, and rotate any key that may have been exposed. <br>


## Reference(s): <br>
- [AI Caption on ClawHub](https://clawhub.ai/fischerlam/ai-caption) <br>
- [Sparki Homepage](https://sparki.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload selected local video files to Sparki and download edited video files to the configured output directory.] <br>

## Skill Version(s): <br>
1.0.12 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
