## Description:

Autonomous crash analysis and bug fixing. Monitors crash reports from Cloudflare D1, deduplicates, analyzes with Codex 5.3 High, generates fixes, and creates PRs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryce](https://clawhub.ai/user/ryce)

### License/Terms of Use:


## Use Case:

Developers and engineers use Crash Fixer to process crash reports, analyze likely root causes with AI, generate code fixes, and open pull requests against a target GitHub repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crash reports and source snippets may be sent to an external AI provider during analysis.

Mitigation: Use only on repositories and crash data where external AI processing is approved, and avoid including secrets or unnecessary personal data in crash reports.

Risk: The skill can create branches, commits, and pull requests from unvalidated model output.

Mitigation: Use a least-privilege GitHub token and require human code review before merging generated changes.

Risk: Dry-run mode avoids pull request creation but can still update crash-reporter state.

Mitigation: Run against a test crash-reporter instance or review expected status changes before using dry-run on production data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryce/skills/crash-fixer)
- [Publisher profile](https://clawhub.ai/user/ryce)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown status text, JSON-shaped AI analysis, generated source code, and GitHub pull request metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports --hours, --limit, and --dry-run command flags; requires GitHub and crash-reporter environment configuration.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
