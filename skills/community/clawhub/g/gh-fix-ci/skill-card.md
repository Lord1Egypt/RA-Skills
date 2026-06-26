## Description: <br>
Use when a user asks to debug or fix failing GitHub PR checks that run in GitHub Actions; use `gh` to inspect checks and logs, summarize failure context, draft a fix plan, and implement only after explicit approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tbeard602](https://clawhub.ai/user/tbeard602) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect failing GitHub Actions checks on pull requests, collect concise failure context, and prepare a focused fix plan. The skill applies changes only after explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the user's existing GitHub CLI authentication to read pull request check status and GitHub Actions logs, which can expose sensitive repository or CI details. <br>
Mitigation: Install and run it only in repositories where this access is acceptable, and avoid sharing log snippets beyond the intended review context. <br>
Risk: Suggested fixes are based on CI logs and may be incomplete or incorrect without developer review. <br>
Mitigation: Review the proposed plan and diffs before approving changes, then rerun the relevant tests and GitHub PR checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tbeard602/gh-fix-ci) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with shell commands and optional JSON from the bundled inspector] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concise CI log snippets, proposed fixes, test summaries, and recheck guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
