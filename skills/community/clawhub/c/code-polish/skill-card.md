## Description: <br>
Pre-release code review skill that runs project checks, analyzes changed code for cleanliness, design reuse, and efficiency issues, reports verified findings, and applies fixes only after approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineering teams use this before committing, pushing, or releasing changes to catch reviewable issues in changed files and receive a grouped Markdown report. After explicit approval, it can make minimal fixes and rerun project checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect local repository contents and run project validation commands as part of its review workflow. <br>
Mitigation: Use it deliberately on repositories you intend to review, confirm the requested checks, and review the generated findings before acting on them. <br>
Risk: Suggested fixes or review findings may be incomplete or incorrect. <br>
Mitigation: The skill requires explicit approval before fixes, validates findings against actual files, and reruns project checks after approved edits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenequm/code-polish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown review report with file and line findings, followed by targeted code edits and check results when fixes are approved.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local validation commands when available, launches focused review agents, and waits for explicit approval before applying fixes.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
