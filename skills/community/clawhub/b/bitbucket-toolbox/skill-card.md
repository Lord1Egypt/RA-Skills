## Description: <br>
Bitbucket Cloud wrapper optimized for Pull Request Code Analysis. Enables the agent to securely review Pull Requests, split large diffs by file, review code structure, and read specific repository files. Ideal for providing automated code reviews or debugging PRs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zan768616253](https://clawhub.ai/user/zan768616253) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect Bitbucket Cloud pull requests, repository files, diffs, comments, commits, and branches so an agent can produce structured code review analysis and debugging guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read Bitbucket repository and pull request data available to the configured token. <br>
Mitigation: Use a dedicated read-only token scoped only to the needed workspace or repositories. <br>
Risk: Full Markdown PR reviews may be saved locally for email pickup, creating retention and distribution risk for review content. <br>
Mitigation: Confirm email recipients before delivery and define retention or cleanup for exported review files. <br>
Risk: The security evidence notes a mismatch between local review export behavior and claims of no local storage. <br>
Mitigation: Review generated files under the skill review directory and document the expected storage behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zan768616253/bitbucket-toolbox) <br>
- [Bitbucket Cloud REST API endpoint](https://api.bitbucket.org/2.0/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [JSON and raw text from Bitbucket queries, plus Markdown for exported PR reviews] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, python3, BITBUCKET_API_TOKEN, and BITBUCKET_WORKSPACE; Bitbucket access is read-only according to the artifact.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
