## Description: <br>
Generate Conventional Commit messages, PR titles, and summaries from git diffs, code snippets, or change descriptions for any project or language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lnguyen1996](https://clawhub.ai/user/Lnguyen1996) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to turn diffs, code snippets, or plain-language change descriptions into commit messages, PR titles, and concise PR summaries. It supports Conventional Commits, Angular-style commits, GitHub squash-merge titles, and plain descriptive output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated commit or PR text may omit important context or misstate the change. <br>
Mitigation: Review the generated message against the actual diff before committing or opening a PR. <br>
Risk: Diffs or code snippets may contain secrets or sensitive proprietary details. <br>
Mitigation: Avoid pasting sensitive diffs into the agent context unless that processing is acceptable for the project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lnguyen1996/commit-message-writer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with commit message, PR title, and PR summary sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commit subjects are expected to be imperative, under 72 characters, and omit a final period when using the documented conventions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
