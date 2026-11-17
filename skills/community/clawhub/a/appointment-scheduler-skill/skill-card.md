## Description:

Schedules appointments with service providers by using PollyReach to place calls, find available times, and report booking outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhugelaing888](https://clawhub.ai/user/zhugelaing888)

### License/Terms of Use:

MIT-0

## Use Case:

People who need phone-based scheduling use this skill to ask an agent to register with PollyReach, place outbound calls to service providers, poll for results, and summarize appointment outcomes or incoming calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a persistent PollyReach token that can make calls, spend credits, answer incoming calls, and retrieve call details.

Mitigation: Store the token with restrictive file permissions, keep it out of chat transcripts and logs, and review balance and call activity before enabling broad use.

Risk: Phone calls and incoming messages may expose personal or business information through recordings, transcripts, summaries, and call detail links.

Mitigation: Use the assigned number only with informed users, avoid sensitive or regulated matters unless approved, and review summaries before sharing them further.

Risk: The security review flags the skill as broader and more privacy-impacting than an appointment scheduler framing suggests.

Mitigation: Present it as a general phone-calling and call-answering integration, and require user confirmation before outbound calls, prompt updates, or public sharing of the assigned number.

Risk: Forwarding remote installation instructions can lead to unreviewed skill installation.

Mitigation: Do not forward the remote SKILL.md installation message to other agents; install only from reviewed artifacts and evidence.

## Reference(s):

- [PollyReach](https://pollyreach.ai)
- [ClawHub Skill Page](https://clawhub.ai/zhugelaing888/skills/appointment-scheduler-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON or text API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, bc, a PollyReach account token, and network access to PollyReach APIs.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
