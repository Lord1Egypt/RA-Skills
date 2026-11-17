## Description:

Place and manage AI-driven phone calls, access transcripts, recordings, call status, and configure inbound call agents via the Bland AI API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xrichyrich](https://clawhub.ai/user/0xrichyrich)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to place and manage Bland AI phone calls from an agent-accessible CLI, including outbound calls, inbound agent setup, transcripts, recordings, number management, balance checks, and call analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real Bland AI calls and perform billable account actions, including purchasing inbound numbers.

Mitigation: Use a dedicated Bland API key with intended permissions, review commands before execution, and check account balance before heavy use.

Risk: Transcripts and recording URLs may contain sensitive call content and can appear in terminal output or logs.

Mitigation: Treat transcript and recording output as sensitive, limit log retention, and avoid sharing terminal output that contains call data.

Risk: The skill may read a broadly shared API key from /root/clawd/.env.

Mitigation: Prefer setting BLAND_API_KEY explicitly for this skill and avoid using shared environment files for production credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xrichyrich/skills/bland)
- [Publisher profile](https://clawhub.ai/user/0xrichyrich)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May output call IDs, call status, account balance, transcript text, analysis results, and temporary recording URLs.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence, created 2026-03-02T09:02:04Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
