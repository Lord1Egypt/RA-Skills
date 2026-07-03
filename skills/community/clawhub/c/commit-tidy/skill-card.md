## Description: <br>
Analyze staged or committed Git changes and recommend split, squash, amend, staging, secret-scan, or commit-message strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and coding agents use this skill to review Git changes, keep commits atomic, draft Conventional Commit messages, and choose safe split, squash, amend, or soft-reset workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: History rewriting guidance can affect shared branches or published commits if used outside branches the user controls. <br>
Mitigation: Treat amend, reset, rebase, and force-push steps as manual actions only on branches the user controls; verify branch state and use force-with-lease after CI status checks. <br>
Risk: The skill includes guidance for installing a persistent global agent hook. <br>
Mitigation: Install the hook only after reviewing its scope and removal path; prefer repository-local or temporary checks when a persistent global hook is not required. <br>
Risk: The workflow is opinionated about English commit messages and commit structure. <br>
Mitigation: Check repository policy before applying the recommendations, especially where local conventions differ from the skill's defaults. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drumrobot/skills/commit-tidy) <br>
- [interactive-amend.md](interactive-amend.md) <br>
- [soft-reset-amend.md](soft-reset-amend.md) <br>
- [staging-discipline.md](staging-discipline.md) <br>
- [security-scan.md](security-scan.md) <br>
- [message-discipline.md](message-discipline.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include changed-file analysis, recommended commit groupings, commit subjects and bodies, and execution commands when requested.] <br>

## Skill Version(s): <br>
0.4.2 (source: server release metadata and CHANGELOG.md, released 2026-06-30) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
