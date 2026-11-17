## Description:

Run A/B evaluation tests for any OpenClaw skill, script, hook, or cron job, including baseline comparison, regression testing, model-swap, prompt variants, trigger accuracy, adversarial robustness, script validation, hook dry-run, cron dry-run, and integration testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyrushuang1995-cmyk](https://clawhub.ai/user/cyrushuang1995-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, preview, run, grade, and report A/B evaluations for OpenClaw skills, scripts, hooks, cron jobs, and integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dry-run and script or cron testing instructions can execute target commands for real without clearly enforced isolation.

Mitigation: Use the preview path first, require exact command review before execution, and run targets only in a disposable sandbox with no inherited credentials and tightly scoped filesystem and network access.

Risk: Evaluating third-party or untrusted skills, scripts, hooks, or cron jobs can expose the agent to unsafe behavior in the target artifact.

Mitigation: Review the target before installing or running it and keep filesystem and network permissions constrained during evaluation.

## Reference(s):

- [AB Test Eval on ClawHub](https://clawhub.ai/cyrushuang1995-cmyk/skills/ab-test-eval)
- [Publisher profile](https://clawhub.ai/user/cyrushuang1995-cmyk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and shell command guidance for evaluation workspaces, assertions, grading files, benchmark reports, and summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce eval case definitions, timing and grading JSON, benchmark summaries, history entries, and user-facing recommendations.]

## Skill Version(s):

2.1.2 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
