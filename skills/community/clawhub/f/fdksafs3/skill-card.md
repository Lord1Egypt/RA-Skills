## Description: <br>
Helps agents use the GitHub CLI for pull requests, workflow runs, issues, and advanced GitHub API queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yequanzheng](https://clawhub.ai/user/yequanzheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to inspect GitHub pull requests, CI checks, workflow runs, issues, and selected API fields through the `gh` CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub CLI commands run with the privileges of the locally authenticated `gh` account. <br>
Mitigation: Confirm the active `gh` account before use and prefer least-privilege GitHub tokens for private or organization repositories. <br>
Risk: `gh api` can query sensitive repository or organization data if used broadly. <br>
Mitigation: Review each `gh api` command before execution and keep commands explicitly scoped to the intended repository. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yequanzheng/fdksafs3) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, JSON] <br>
**Output Format:** [Markdown with inline bash code blocks and optional GitHub CLI JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should be scoped with `--repo owner/repo` when not already in a git repository.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
