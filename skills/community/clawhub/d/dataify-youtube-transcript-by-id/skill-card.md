## Description: <br>
Submit Dataify YouTube Transcript by Video ID Builder tasks for the YouTube subtitle file collection tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit Dataify Builder jobs that collect YouTube subtitles or transcripts by video ID, then receive the created task ID, status, and dashboard link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit Dataify transcript collection tasks and may be invoked implicitly. <br>
Mitigation: Ask the user to confirm parameters before submitting a Builder task, especially when using a saved DATAIFY_API_TOKEN. <br>
Risk: Submitted YouTube video IDs and requested transcript settings are sent to Dataify. <br>
Mitigation: Avoid submitting private or sensitive URLs or identifiers unless Dataify handling is acceptable to the user. <br>
Risk: A Dataify API TOKEN is required for task submission. <br>
Mitigation: Do not persist or use a token silently; use the saved DATAIFY_API_TOKEN only when appropriate and ask before saving a newly provided token. <br>


## Reference(s): <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify Login](https://dashboard.dataify.com/login?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions and JSON task summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns or explains task_id, status, submitted parameters, Dataify dashboard URL, and API TOKEN setup guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
