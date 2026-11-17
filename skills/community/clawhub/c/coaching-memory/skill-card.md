## Description:

Helps AI agents track coaching goals and progress using BlueColumn persistent memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can equip coaching agents to recall prior goals, personalize responses, and store concise progress notes through BlueColumn's API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coaching summaries and progress notes may be sent to an external service without clear user consent, minimization, or retention guidance.

Mitigation: Get explicit user consent before storing coaching memory, keep notes brief and redacted, and avoid sensitive personal details unless retention and deletion controls are clear.

Risk: Automatic recall and storage can cause inaccurate, stale, or overly broad coaching context to influence later responses.

Mitigation: Review recalled context before using it, let users correct stored summaries, and store only concise post-interaction summaries.

Risk: The skill requires a BlueColumn API key for external API calls.

Mitigation: Load the key only from a secret store or approved tool context, and never include it in generated responses, logs, or stored coaching notes.

## Reference(s):

- [BlueColumn API reference](https://bluecolumn.ai/docs)
- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/coaching-memory)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown]

**Output Format:** [Markdown guidance with inline curl examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key (bc_live_*); sends coaching summaries and recall queries to an external BlueColumn service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
