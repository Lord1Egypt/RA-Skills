## Description: <br>
Analyze failed GitHub Action jobs for a pull request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect failed GitHub Actions jobs for a pull request or job URL and summarize the likely failure cause, relevant errors, test names, and log excerpts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use GitHub credentials while analyzing CI failures. <br>
Mitigation: Use the least-privilege GitHub token that can access the target pull request or job logs. <br>
Risk: CI logs may contain secrets or sensitive data and may be sent to Claude for analysis. <br>
Mitigation: Avoid running the skill on sensitive logs unless sharing that content with Claude is acceptable. <br>
Risk: Debug mode can expose token and cost details. <br>
Mitigation: Use `--debug` only when those details are needed for troubleshooting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/fix-build-agentops-analyze-ci) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Concise text or Markdown failure analysis with relevant log snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include root cause, error messages, test names, and CI log excerpts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
