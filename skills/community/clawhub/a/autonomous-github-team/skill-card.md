## Description:

Autonomous GitHub Team monitors a GitHub repository, detects bugs, creates fixes, opens pull requests, and supports release automation while requiring GitHub write credentials and external script execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[captainsvbot](https://clawhub.ai/user/captainsvbot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate automated GitHub repository maintenance, bug-fix pull requests, issue handling, and guarded release workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires GitHub repository write access through a personal access token.

Mitigation: Use a dedicated fine-grained token scoped to one disposable or test repository with only contents, pull requests, and issues permissions.

Risk: The skill directs users to run external bash scripts with write-scoped credentials.

Mitigation: Audit the upstream scripts and verify the exact tagged commit before running any agent commands.

Risk: Automated pull request and release workflows can affect protected branches or production repositories.

Mitigation: Test in an isolated fork, enable branch protection, and require human review before production merges or releases.

Risk: Credential files such as config.env can expose high-privilege secrets if committed or shared.

Mitigation: Keep token configuration out of version control and scan for secrets before publishing changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/captainsvbot/skills/autonomous-github-team)
- [AutonomousGitHubTeam install repository](https://github.com/captainsvbot/AutonomousGitHubTeam.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git, bash, curl, python3, GH_TOKEN, and TARGET_REPO.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
