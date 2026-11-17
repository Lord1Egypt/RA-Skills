## Description:

AI Interview Simulator helps agents use Candaigo's API to browse jobs, create and run group interview rooms, exchange messages, upload resumes, and retrieve interview history and evaluations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hangeaiagent](https://clawhub.ai/user/hangeaiagent)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to interact with Candaigo's remote AI group interview simulation service: register API access, create or join interview rooms, submit messages, advance AI participation, upload resumes, and review results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send resumes, interview chat logs, participant information, and evaluation data to Candaigo's remote service.

Mitigation: Use it only when Candaigo is trusted for this data, avoid uploading unnecessary personal details, and review the skill before installing or running resume and result workflows.

Risk: API keys grant access to protected interview resources and can be exposed if copied into shared code or logs.

Mitigation: Protect API keys, avoid hardcoding them in public code, and rotate or revoke credentials if exposure is suspected.

Risk: Polling loops for messages and interview advancement can continue making remote requests after a session ends.

Mitigation: Stop polling loops when the interview session is done and respect the documented rate guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hangeaiagent/skills/ai-interview-simulator-candaigo)
- [Publisher profile](https://clawhub.ai/user/hangeaiagent)
- [Candaigo API base URL](https://me.candaigo.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with API endpoint descriptions and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API-key authentication guidance, polling recommendations, request limits, and example JSON responses.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
