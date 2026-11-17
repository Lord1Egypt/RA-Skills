## Description:

Get your AI agent productive in 5 minutes with an environment scan, skill recommendations, and exact install commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[certainlogicai](https://clawhub.ai/user/certainlogicai)

### License/Terms of Use:

Business Source License 1.1

## Use Case:

External users, developers, and teams use this skill to scan an OpenClaw environment, choose a goal-specific starter stack, and generate onboarding reports, install checklists, setup scripts, verification reports, weekly checkups, and team onboarding exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release can generate executable bulk-install scripts for mutable third-party skills.

Mitigation: Review generated setup.sh files before running them and inspect each recommended skill's publisher, version, and contents before installation.

Risk: Recommended skills are suggestions rather than verified-safe dependencies.

Mitigation: Treat recommendations as advisory, scan or inspect each skill before installation, and test installed skills before relying on them.

Risk: The local environment scan and verification behavior may miss custom setups or runtime failures.

Mitigation: Use generated reports as a starting point, confirm detected paths and versions, and perform task-level checks after setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/certainlogicai/skills/ai-agent-onboarding-wizard)
- [Publisher profile](https://clawhub.ai/user/certainlogicai)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown reports with inline shell commands; optional bash setup scripts and team export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write onboarding reports, verification reports, weekly checkup state, setup scripts, and team export bundles to local output directories.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
