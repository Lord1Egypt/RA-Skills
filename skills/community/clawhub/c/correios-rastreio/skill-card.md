## Description:

Tracks Correios packages through the official API, with support for single or multiple tracking codes, local history, and favorites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runawaydevil](https://clawhub.ai/user/runawaydevil)

### License/Terms of Use:


## Use Case:

Portuguese-speaking users and agents use this skill to check Brazilian Correios shipment status, review recent tracking history, and manage favorite tracking codes from a Node.js CLI.

### Deployment Geography for Use:

Global; the workflow is Brazil-focused because it depends on Correios tracking codes and Correios API access.

## Known Risks and Mitigations:

Risk: Live tracking requires a Correios API key supplied through CORREIOS_API_KEY.

Mitigation: Provide the key only through the environment, rotate it if exposed, and avoid pasting it into prompts, logs, or shared command transcripts.

Risk: Tracking codes, history entries, and favorites are saved locally in the skill directory.

Mitigation: Review or delete the local data file before sharing the workspace, publishing artifacts, or running the skill in a shared environment.

Risk: The security guidance notes dependency caveats for the npm package set.

Mitigation: Audit or update npm dependencies before installation in managed or production environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/runawaydevil/skills/correios-rastreio)
- [Publisher Profile](https://clawhub.ai/user/runawaydevil)
- [Correios Developer Portal](https://developers.correios.com.br)
- [Correios API Base](https://api.correios.com.br)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Console-oriented text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CORREIOS_API_KEY for live tracking requests and stores tracking history and favorites locally in the skill directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
