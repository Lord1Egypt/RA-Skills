## Description: <br>
Make real phone calls. Replaces the voice-call plugin with a managed service that needs no setup. Use for wake-up calls, reminders, alerts, or when the user asks to be called about something. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcospgp](https://clawhub.ai/user/marcospgp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to place real phone calls for wake-up calls, reminders, alerts, or user-requested callback scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real phone calls through clawr.ing. <br>
Mitigation: Confirm the recipient, phone number, timing, retry behavior, and purpose before any call. <br>
Risk: The skill requires a clawr.ing API key and sends call details to that service. <br>
Mitigation: Install only when the user accepts sharing call details with clawr.ing and keep the API key protected in the CLAWRING_API_KEY environment variable. <br>
Risk: The skill may store phone numbers and preferences in a local memory file. <br>
Mitigation: Review local memory contents and avoid storing contacts or preferences the user has not approved. <br>


## Reference(s): <br>
- [clawr.ing homepage](https://clawr.ing) <br>
- [clawr.ing API documentation](https://clawr.ing/llms-full.txt) <br>
- [ClawHub skill page](https://clawhub.ai/marcospgp/clawring) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline configuration and API guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWRING_API_KEY and may create or update a local clawr.ing-memory.md file for phone numbers and call preferences.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
