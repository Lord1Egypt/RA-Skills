## Description:

ClawReach helps users bind a ClawReach Agent account, build a social matching profile, poll for pending match messages, and generate agent replies on the user's behalf.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiwenbing](https://clawhub.ai/user/jiwenbing)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to connect a ClawReach account, create a matching profile, and let an agent screen social matches through guided profile collection and automated reply workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for ClawReach login credentials and stores a reusable access token in a predictable local file.

Mitigation: Use it only with a trusted ClawReach service, prefer OAuth or a scoped token when available, and store secrets with a secure credential store rather than plaintext workspace memory.

Risk: The background poller can send match messages and final match decisions automatically.

Mitigation: Require explicit opt-in before polling, keep approval gates for outbound messages and conclusions, and provide a clear way to stop the cron job.

Risk: Automated social screening may misrepresent the user's intent or disclose sensitive personal preferences.

Mitigation: Let the user review the generated profile and public card before publishing, and avoid collecting or sending information beyond the matching fields the user intentionally provides.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, API Calls, Guidance]

**Output Format:** [Markdown guidance with JSON examples, HTTP request shapes, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes instructions for account binding, token storage, profile upload, polling setup, reply generation, and match conclusion.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
