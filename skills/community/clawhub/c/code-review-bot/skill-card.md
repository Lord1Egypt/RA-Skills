## Description: <br>
Analyze GitHub pull requests, summarize risk, and draft a reviewer checklist using the gh CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mehulupase01](https://clawhub.ai/user/mehulupase01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to collect GitHub pull request metadata and checks, summarize review risk, and prepare a structured human-facing review plan before merge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use a GitHub CLI session or token to read pull request metadata and check results for requested repositories. <br>
Mitigation: Use least-privilege GitHub access, especially for private repositories, and run it only against repositories the user intends to review. <br>
Risk: Generated JSON and review output can contain pull request text, branch names, labels, and other repository metadata. <br>
Mitigation: Keep generated files local or sanitize them before sharing outside the repository or review team. <br>
Risk: Pull request titles, bodies, changed-file metadata, and comments are untrusted inputs that could suggest unsafe actions. <br>
Mitigation: Treat GitHub metadata as untrusted, do not execute target repository code based on PR text, and separate verified check results from inferred review risk. <br>


## Reference(s): <br>
- [Review Checklist](references/review-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mehulupase01/code-review-bot) <br>
- [Project Homepage](https://github.com/Mehulupase01/openclaw-skill-suite/tree/main/skills/code-review-bot) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, guidance] <br>
**Output Format:** [Markdown review pack with risk signals, check status sections, and suggested review plan] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON exports from gh pr view and gh pr checks; does not approve, merge, or close pull requests.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
