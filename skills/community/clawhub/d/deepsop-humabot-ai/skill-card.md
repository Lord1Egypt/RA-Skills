## Description: <br>
DeepSop工作台 helps agents turn natural-language sales requests into DeepSOP customer mining, email, phone, SMS, and outbound-call-scene workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kukuoai](https://clawhub.ai/user/kukuoai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and growth teams use this skill to submit DeepSOP customer discovery, email, phone, SMS, and outbound-call-scene tasks from conversational instructions. Agents can also query task results, summarize campaign metrics, and return spreadsheet reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive DeepSOP API key. <br>
Mitigation: Install only in trusted workspaces, store the key in the environment, and rotate or remove DEEPSOP_API_KEY when the workspace is no longer trusted. <br>
Risk: Automatic result queries can send generated sales reports or customer data to chat channels. <br>
Mitigation: Confirm the destination chat or channel before use and avoid sharing customer lists or outreach results in shared channels unintentionally. <br>
Risk: Follow-up jobs can query sales results without a fresh authorization check. <br>
Mitigation: Use the skill only where scheduled DeepSOP result queries and chat-file delivery are acceptable for the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kukuoai/deepsop-humabot-ai) <br>
- [DeepSOP login](https://ai.deepsop.com/login?source=3) <br>
- [DeepSOP registration](https://ai.deepsop.com/register?source=3) <br>
- [DeepSOP API base](https://ai.deepsop.com/prod-api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown or JSON-oriented task guidance with shell command snippets and generated xlsx report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPSOP_API_KEY and may submit or query sales automation tasks through DeepSOP APIs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
