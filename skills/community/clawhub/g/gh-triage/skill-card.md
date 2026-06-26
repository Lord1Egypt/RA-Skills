## Description: <br>
Automatically scans GitHub repositories to label, comment on, assign, and optionally fix issues and pull requests for maintainers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gruted](https://clawhub.ai/user/gruted) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and repository maintainers use this skill to automate routine GitHub issue and pull request triage, including labels, assignment, comments, reports, and optional lightweight fix pull requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically change GitHub repositories while authenticated with a GitHub token. <br>
Mitigation: Install only for trusted repositories and use a dedicated least-privilege GitHub token. <br>
Risk: The optional auto-fix behavior can run repository code and tooling on the host. <br>
Mitigation: Disable or sandbox auto-fix unless intentional, and add dry-run or human approval before pushes and pull requests. <br>
Risk: Temporary working directories may retain token-bearing git configuration. <br>
Mitigation: Clean temporary work directories after use and avoid persistent credential material in cloned repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gruted/gh-triage) <br>
- [Publisher profile](https://clawhub.ai/user/gruted) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [GitHub issue and pull request updates, console text, reports, configuration JSON, and optional code changes in pull requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses repository configuration and a GitHub token; optional auto-fix can run local shell commands against cloned repositories.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
