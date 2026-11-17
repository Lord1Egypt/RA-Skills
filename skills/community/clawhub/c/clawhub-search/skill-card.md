## Description:

Searches the ClawHub Skills marketplace to help agents find OpenClaw community skills by keyword and sort order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahongting](https://clawhub.ai/user/mahongting)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search the ClawHub Skills marketplace, compare results by popularity or recency, and identify skills to inspect or install.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install example uses an unpinned ClawHub CLI command that can change the local skill environment.

Mitigation: Prefer a pinned and reviewed CLI version, inspect the selected skill before installation, and run installs in an isolated environment.

Risk: The skill requires a ClawHub API token for authenticated search requests.

Mitigation: Store the token in CLAWHUB_TOKEN, avoid embedding token values in commands or documents, and run the skill without unrelated secrets in the environment.

## Reference(s):

- [ClawHub Search skill page](https://clawhub.ai/mahongting/skills/clawhub-search)
- [ClawHub Skills API](https://clawhub.ai/api/v1/skills)
- [ClawHub Skills marketplace](https://clawhub.ai/skills)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown guidance with inline bash and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a CLAWHUB_TOKEN environment variable and works with JSON responses from the ClawHub Skills API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
