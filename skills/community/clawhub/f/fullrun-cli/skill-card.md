## Description:

Manage Google Ads campaigns -- diagnose, optimize, and create campaigns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuckerschreiber](https://clawhub.ai/user/tuckerschreiber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent inspect Google Ads account health, review campaign and keyword performance, and run guarded optimization workflows through the Fullrun CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger automatic Google Ads account changes through the Fullrun CLI.

Mitigation: Require manual approval before running automatic optimizations against live ad accounts, and run triage before taking action.

Risk: The skill relies on a sensitive Fullrun API key.

Mitigation: Use a secret manager or safer login flow, and avoid passing the API key on the command line.

Risk: The skill requires a globally installed CLI package that is not pinned by the skill artifact.

Mitigation: Install only a verified Fullrun package and version before enabling the skill.

## Reference(s):

- [Fullrun skill page](https://clawhub.ai/tuckerschreiber/skills/fullrun-cli)
- [tuckerschreiber publisher profile](https://clawhub.ai/user/tuckerschreiber)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced CLI returns structured JSON by default and uses exit codes for success, errors, and guardrail blocks.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
