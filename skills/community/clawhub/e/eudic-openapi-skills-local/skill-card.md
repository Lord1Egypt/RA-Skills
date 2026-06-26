## Description: <br>
Provides agent-facing Eudic OpenAPI guidance for managing vocabulary books, words, notes, and English pronunciation scoring across Eudic, French Assistant, German Assistant, and Spanish Assistant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ink-kai](https://clawhub.ai/user/ink-kai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and language-learning users use this skill to let an agent call Eudic OpenAPI endpoints for vocabulary list management, word lookup, note management, and English voice scoring. It is useful when the agent needs to prepare curl-based API requests that require a user-provided Eudic API token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A valid Eudic API token gives the agent access to the user's Eudic OpenAPI account actions. <br>
Mitigation: Keep the token private, avoid logging it, and provide it only when the user intends the agent to call Eudic. <br>
Risk: The skill can rename or delete vocabulary books, words, and notes. <br>
Mitigation: Confirm destructive or renaming requests by exact item name and ID before executing the API call. <br>
Risk: English pronunciation scoring uploads an audio file to Eudic. <br>
Mitigation: Upload only audio files the user explicitly intends to send for scoring. <br>
Risk: Frequent API calls may trigger documented Eudic rate limits. <br>
Mitigation: Keep request volume within the documented limits and pause when the API reports frequency restrictions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ink-kai/eudic-openapi-skills-local) <br>
- [Eudic OpenAPI authorization](https://my.eudic.net/OpenAPI/Authorization) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with curl commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Eudic API token and supports English, French, German, and Spanish language parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
