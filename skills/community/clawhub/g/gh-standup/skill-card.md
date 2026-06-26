## Description: <br>
Generate a GitHub standup summary covering the period since the last standup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zerone0x](https://clawhub.ai/user/zerone0x) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to summarize merged pull requests and direct commits for standups, work summaries, and weekly updates across a repository or organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated summaries may include private repository names, pull request titles, commit messages, and links from the user's authenticated GitHub access. <br>
Mitigation: Prefer repository-scoped summaries when possible, use organization scope only when intended, and review the generated text before sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zerone0x/gh-standup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown standup summary with repository activity links and shell command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated GitHub CLI and Python 3.10+; supports repository or organization scope, standup days, and author filtering.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
