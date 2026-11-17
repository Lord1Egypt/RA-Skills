## Description:

Interact with Codeberg using the `tea` CLI. Use `tea issue`, `tea pr`, `tea actions`, and `tea api` for issues, PRs, Actions, and advanced queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[razzeee](https://clawhub.ai/user/razzeee)

### License/Terms of Use:


## Use Case:

Developers and repository maintainers use this skill to manage Codeberg issues, pull requests, CI/CD actions, and advanced API queries through the Tea CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Codeberg operations can expose or alter repository data if broad credentials are used.

Mitigation: Use a narrowly scoped token and avoid pasting tokens directly into logged shell commands.

Risk: Repository secret commands may expose sensitive CI/CD metadata.

Mitigation: Run repository secret commands only for repositories you administer and only when that sensitive metadata is needed.

## Reference(s):

- [Codeberg](https://codeberg.org)
- [ClawHub Codeberg Skill](https://clawhub.ai/razzeee/skills/codeberg)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the `tea` CLI; some examples use `jq` for filtering.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
