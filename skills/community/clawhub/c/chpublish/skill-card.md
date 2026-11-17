## Description:

ClawHub 发布助手 helps developers publish local skills to the ClawHub marketplace by checking the skill directory, preparing release parameters, running the ClawHub CLI publish command, and verifying the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to publish new or updated local skills to ClawHub while checking login state, release history, slug, version, changelog, tags, and publish results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run ClawHub CLI commands that publish or update content under the user's account.

Mitigation: Use it only for intentional ClawHub releases and verify the target directory, slug, version, changelog, tags, and displayed command arguments before publishing.

Risk: Shell-built publish commands can be exposed to command injection if untrusted skill metadata or changelog text is used as command input.

Mitigation: Avoid untrusted metadata or changelog text unless the workflow is changed to pass command arguments safely without shell interpolation.

Risk: Broad activation language can trigger publishing behavior when the user did not intend an account-changing action.

Mitigation: Invoke the skill only for explicit publishing requests and require confirmation of release parameters before running publish commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and release parameter values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose and execute ClawHub CLI commands after gathering and confirming release parameters.]

## Skill Version(s):

2.1.0 (source: server release evidence, released 2026-04-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
