## Description: <br>
Multi-repo PR monitoring and triage agent that scans GitHub repositories for open PRs, prioritizes by staleness, review status, and CI state, and generates a structured Markdown triage summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanxevo3](https://clawhub.ai/user/lanxevo3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to monitor open pull requests across multiple GitHub repositories and surface the PRs most likely to need review, CI attention, or merge follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads pull request metadata from every repository named by the user through the authenticated GitHub CLI. <br>
Mitigation: Use a GitHub token with only the repository access needed for the intended triage run, and provide only repositories that should be inspected. <br>
Risk: The shell helper depends on jq in addition to the authenticated GitHub CLI. <br>
Mitigation: Prefer the Python triage script for standard use, or confirm jq is installed before using the shell helper. <br>


## Reference(s): <br>
- [Fleet PR Agent on ClawHub](https://clawhub.ai/lanxevo3/fleet-pr-agent) <br>
- [Publisher profile: lanxevo3](https://clawhub.ai/user/lanxevo3) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown triage report with prioritized PR sections and summary counts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print the report to standard output or write it to a Markdown file when an output path is provided.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
