## Description: <br>
Run a structured code review as a closeout check on a local or PR branch before commit or ship. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thanosbao](https://clawhub.ai/user/thanosbao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Autoreview to run structured AI-assisted code review on local changes, commits, or branch/PR diffs before committing, shipping, or closing out work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper reads selected git changes and may include untracked file contents in local mode before sending a review bundle to the configured AI review engine. <br>
Mitigation: Review untracked files and secrets before running the helper, and use commit or branch mode when a narrower review target is needed. <br>
Risk: A pasted or untrusted parallel test command can execute with the user's local shell privileges. <br>
Mitigation: Run only trusted commands with --parallel-tests and inspect copied commands before execution. <br>
Risk: Review findings can be incorrect or speculative. <br>
Mitigation: Treat findings as advisory, verify each accepted finding in the relevant code path, and rerun focused tests and review after making fixes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thanosbao/autoreview) <br>
- [Publisher profile](https://clawhub.ai/user/thanosbao) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown and structured review findings, with optional shell commands and JSON output from the helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review output is advisory; users are expected to verify findings against the real code and rerun focused tests and review after accepted fixes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
