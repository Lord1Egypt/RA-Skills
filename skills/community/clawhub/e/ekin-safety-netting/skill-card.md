## Description:

Automated clinical safety netting for NHS GPs. Follows up with patients after appointments, checks for red flag symptoms, escalates to GP when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ekin-kahraman](https://clawhub.ai/user/ekin-kahraman)

### License/Terms of Use:

MIT-0

## Use Case:

NHS GP teams and clinical operations staff can use this agent to follow up with patients after appointments, check responses for configured red flag symptoms, and escalate concerning or unclear outcomes to a GP. It supports, but does not replace, clinical judgement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles identifiable patient medical data and patient responses.

Mitigation: Use an approved encrypted clinical datastore with documented retention and deletion rules before real clinical deployment.

Risk: The skill requires broad backend credentials, including a Supabase service-role key.

Mitigation: Replace broad credentials with narrowly scoped credentials and restrict access to only the records and operations required for follow-up.

Risk: Patients may be contacted through multiple channels, which can expose clinical information or reach unverified recipients.

Mitigation: Verify patient consent and contact channels, and minimize message content to the least clinical detail needed.

Risk: Learning data from patient interactions could preserve sensitive clinical details or reinforce incorrect matching behavior.

Mitigation: Apply governance to learning data, de-identify where possible, and require clinical review before changing red flag matching behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ekin-kahraman/skills/ekin-safety-netting)
- [ClawHub publisher profile](https://clawhub.ai/user/ekin-kahraman)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration, Records]

**Output Format:** [Markdown or plain text messages with structured status and audit details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate patient follow-up messages, GP escalation notices, resolution status, matched red flags, and audit trail entries.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
