## Description:

Run a short end-of-day debrief that reflects on the day, extracts action items and open loops, previews tomorrow, and stores the result in Fulcra as a structured annotation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keng009](https://clawhub.ai/user/keng009)

### License/Terms of Use:

MIT-0

## Use Case:

Fulcra users use this skill as a light evening coaching workflow to review the day, capture meeting feedback, wins, open loops, and action items, and prepare for tomorrow. It is intended for personal concierge-style reflection where calendar context and structured Fulcra annotations are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Fulcra or Attio traffic could be redirected if environment variables such as FULCRA_API_BASE, ATTIO_API_BASE, or FULCRA_CLI_COMMAND are untrusted.

Mitigation: Install and run the skill only in a trusted environment with known-good Fulcra tooling and controlled environment variables.

Risk: The package includes broader shared CRM/Fulcra helpers than the evening debrief workflow itself needs.

Mitigation: Review the packaged helper scripts and grant credentials only with the minimum authority needed for the intended Fulcra debrief workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keng009/skills/fulcra-evening-debrief)
- [Fulcra API](https://api.fulcradynamics.com)
- [Attio API](https://api.attio.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Conversational guidance with JSON payloads and shell commands for Fulcra annotation reads and writes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write an Evening Debrief Fulcra annotation when the user provides debrief content and authenticated Fulcra tooling is available.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
