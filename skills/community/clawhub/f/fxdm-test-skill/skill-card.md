## Description:

Manage Trello boards, lists, and cards via the Trello REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fxdm41202425](https://clawhub.ai/user/fxdm41202425)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Trello boards, lists, and cards from an agent session with Trello REST API commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Trello API token can read and change Trello data.

Mitigation: Use a least-privileged token and install the skill only when the agent should access and modify Trello.

Risk: Commands that use the wrong board, list, or card ID can change unintended Trello content.

Mitigation: Verify board, list, and card IDs before write commands and test first on a non-production board.

Risk: API keys and tokens can be exposed through logged shell commands or verbose CI traces.

Mitigation: Avoid running examples in logged shells or CI jobs with verbose tracing enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fxdm41202425/skills/fxdm-test-skill)
- [Trello REST API documentation](https://developer.atlassian.com/cloud/trello/rest/)
- [Trello API key and token page](https://trello.com/app-key)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq plus TRELLO_API_KEY and TRELLO_TOKEN environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
