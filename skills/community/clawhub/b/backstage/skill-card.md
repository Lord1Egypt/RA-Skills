## Description: <br>
Backstage companion helps agents run an anti-drift project workflow that loads context, checks project health, and reports status before commits or session handoffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nonlinear](https://clawhub.ai/user/nonlinear) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and trusted teams use this skill to keep AI-assisted project work aligned with roadmap, changelog, branch, and checks before commits or session transitions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local and project shell scripts and use checks loaded from global or project directories. <br>
Mitigation: Install only in trusted personal or team projects, review all .sh and .md checks before running, and avoid broad casual triggers in untrusted repositories. <br>
Risk: The update workflow can pull executable checks from an unpinned GitHub source and replace or delete local global-check content. <br>
Mitigation: Inspect update changes before approving, keep changes under git history for rollback, and only trust the configured upstream repository. <br>


## Reference(s): <br>
- [Backstage upstream repository](https://github.com/nonlinear/backstage) <br>
- [ClawHub skill page](https://clawhub.ai/nonlinear/backstage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style status reports, terminal text, shell command guidance, and generated Mermaid snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide updates to project documentation and local checks after user confirmation.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
