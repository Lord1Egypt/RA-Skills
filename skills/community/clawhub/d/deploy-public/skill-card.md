## Description: <br>
Private-to-public repo sync. Copies everything except ai/ to the public mirror. Creates PR, merges, syncs releases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release maintainers use this skill to publish a private repository to its public GitHub mirror, create and merge a sync PR, and carry release notes forward. It is intended for repositories that already have a private-to-public counterpart workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish private repository contents to a public GitHub repository. <br>
Mitigation: Confirm the target public repository and exclusions before running, and run secret scanning on the content to be published. <br>
Risk: The skill can merge PRs, edit releases, delete public branches, and publish npm packages. <br>
Mitigation: Use narrowly scoped GitHub and npm credentials, and review the affected branches, releases, and package versions before execution. <br>
Risk: The security assessment flags use of local 1Password-backed credentials for npm publishing. <br>
Mitigation: Verify the local credential source and prefer tokens limited to the intended packages and release workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/deploy-public) <br>
- [Publisher profile](https://clawhub.ai/user/parkertoddbrooks) <br>
- [AI DevOps Toolbox](https://github.com/wipcomputer/wip-ai-devops-toolbox) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires git, gh, bash, a local private repository path, and a target public GitHub repository.] <br>

## Skill Version(s): <br>
1.9.72 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
