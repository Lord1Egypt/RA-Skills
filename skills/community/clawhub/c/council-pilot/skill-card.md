## Description: <br>
Council Pilot builds an expert forum from public sources, uses it to score project maturity, generates code, debugs, rescores, and can submit the resulting project to GitHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wd041216-bit](https://clawhub.ai/user/wd041216-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn a project idea into an expert-guided build loop that researches public sources, forms an advisory council, scores maturity, generates code, verifies the result, and prepares a GitHub submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can autonomously research online, edit repositories, run shell commands, and potentially publish a GitHub pull request. <br>
Mitigation: Run it in a sandbox or disposable branch, review generated files and build logs, and require manual confirmation before git push or PR creation. <br>
Risk: Generated repository changes or logs could accidentally include secrets or private details. <br>
Mitigation: Review all generated files and build logs for secrets or private information before deployment or publication. <br>


## Reference(s): <br>
- [Council Pilot ClawHub page](https://clawhub.ai/wd041216-bit/council-pilot) <br>
- [Project homepage from ClawHub metadata](https://github.com/wd041216-bit/council-pilot) <br>
- [Build Integration](references/build-integration.md) <br>
- [Council Protocol](references/council-protocol.md) <br>
- [GitHub Submission](references/github-submission.md) <br>
- [Loop State Machine](references/loop-state-machine.md) <br>
- [Expert Profile Contract](references/profile-contract.md) <br>
- [Maturity Scoring Rubric](references/scoring-rubric.md) <br>
- [Source Gates](references/source-gates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, JSON state and report files, code changes, shell commands, and GitHub PR metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May edit repositories, run verification commands, and prepare or create GitHub pull requests depending on the active agent permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
