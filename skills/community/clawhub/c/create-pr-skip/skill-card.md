## Description: <br>
Creates a pull request with a standardized description template based on the current branch changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect branch changes, summarize the work, draft a conventional pull request title and body, create the pull request with the GitHub CLI, and apply appropriate labels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may place sensitive or inaccurate repository details into a pull request title, body, labels, or issue references. <br>
Mitigation: Review the generated PR title, body, labels, and related issue references before relying on them, especially for private repositories or sensitive changes. <br>
Risk: A pull request could be created from incomplete branch evidence if the branch, evidence, template, or create gates are skipped. <br>
Mitigation: Run the gates in order and only report a pull request as created after gh returns a PR URL, number, or identifier. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown PR title and body text with GitHub CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or edit a GitHub pull request through existing gh authentication after the skill's gates pass.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
