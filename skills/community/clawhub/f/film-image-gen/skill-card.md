## Description: <br>
Film Image Gen helps agents generate film concept art, posters, storyboards, and character designs through the Youchuang AIGC API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taosiuman](https://clawhub.ai/user/taosiuman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creative teams, developers, and agents use this skill to turn visual briefs into generated film and television imagery, including concept art, posters, storyboards, character designs, and mood boards. It guides model selection, request construction, asynchronous polling, and result handling for the external image-generation API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes plaintext third-party API keys. <br>
Mitigation: Rotate and remove bundled keys before use; require user-provided credentials or a managed secret mechanism. <br>
Risk: Prompts and reference image URLs are sent to an external image-generation API. <br>
Mitigation: Use only non-sensitive prompts and image URLs, and disclose/review external data handling before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/taosiuman/film-image-gen) <br>
- [Publisher profile](https://clawhub.ai/user/taosiuman) <br>
- [Youchuang AIGC API endpoint](https://api.lk888.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown instructions and PowerShell command output with generated image result URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit asynchronous image-generation jobs, poll for completion, and return result URLs, task status, cost, and elapsed time.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json; artifact SKILL.md footer says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
