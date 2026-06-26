## Description: <br>
Guides agents through FlashRev-powered email outreach workflows using the flashrev-mailer npm CLI, including campaign planning, drafting, live send approval, reply triage, scheduling, and optional AI auto-reply. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flashlabs-ai](https://clawhub.ai/user/flashlabs-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external business users use this skill to have an agent prepare, inspect, commit, monitor, and follow up on FlashRev email outreach while preserving human approval for live sends and other production actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent initiate real outbound email campaigns and modify production campaign state. <br>
Mitigation: Require explicit user approval for dry runs, live sends, send-now, pause or resume, rescheduling, direct replies, step removal, and deletion before running the relevant command. <br>
Risk: FlashRev API keys and campaign workspace data may expose sensitive credentials, recipients, drafts, schedules, inbox metadata, and profile data. <br>
Mitigation: Keep the API key only in the operator shell environment, avoid writing secrets to configuration or chat output, and use the .flashrev workspace only on a trusted machine. <br>
Risk: AI auto-reply can send LLM-generated messages to prospects on the user's behalf. <br>
Mitigation: Show the exact auto-reply prompt verbatim, obtain explicit approval before enabling it, and default to disabled whenever the prompt or authorization is ambiguous. <br>


## Reference(s): <br>
- [FlashRev API Contract](references/api_contract.md) <br>
- [Flashrev Mailer ClawHub Release](https://clawhub.ai/flashlabs-ai/flashrev-mailer) <br>
- [FlashRev API Key Settings](https://info.flashlabs.ai/settings/privateApps) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, json] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-oriented CLI output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FLASHREV_MAILER_AI_MODE=1 or --ai-mode for structured list, view, and error output.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata and skill title) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
