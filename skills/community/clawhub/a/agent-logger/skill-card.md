## Description:

Agent Logger analyzes agent run logs for errors, token spikes, and failures with stdlib-only offline output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Agent Logger to scan local agent run logs for errors, warnings, suspected token spikes, and failure signals, with text or JSON output for debugging and dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation includes an unpinned raw-GitHub main-branch command for downloading executable Python.

Mitigation: Install only from the reviewed package copy or a pinned, verified release.

Risk: The auxiliary verifier can execute Python files from target folders during product checks.

Mitigation: Run ci/verify_product.py only on trusted folders or inside a disposable sandbox with no secrets or network access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itspremkumar/skills/agent-logger)

## Skill Output:

**Output Type(s):** [text, json, analysis]

**Output Format:** [Plain text or JSON CLI report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline local analysis of .log, .txt, and .json files; error samples are capped at five.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
