## Description:

Analyze failed GitHub Action jobs for a pull request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CI maintainers use this skill to inspect failed GitHub Actions jobs for a pull request or job URL and summarize root causes, error messages, affected tests, and relevant log snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses GitHub Actions logs and may surface sensitive information from CI output.

Mitigation: Use a least-privilege GitHub token, avoid debug output in shared logs, and treat returned log snippets as potentially sensitive.

Risk: The skill analyzes CI failures with Claude, so summaries may omit or misstate details from the underlying logs.

Mitigation: Review the cited error messages, test names, and relevant log snippets before acting on the analysis.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Concise markdown analysis with relevant log snippets and command-oriented usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CI failure summaries, root-cause notes, error messages, test names, and selected GitHub Actions log excerpts.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
