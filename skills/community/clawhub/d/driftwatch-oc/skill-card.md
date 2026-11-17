## Description:

Scan OpenClaw workspaces for truncation risk, compaction anchor health, workspace hygiene, and drift trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danandbub](https://clawhub.ai/user/danandbub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use Driftwatch to inspect workspace bootstrap files for truncation, missing anchor sections, hygiene issues, and drift trends before those issues degrade agent behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scan metadata and HTML reports may persist under ~/.driftwatch.

Mitigation: Review generated reports and retention settings before enabling save, history, or recurring scans; remove local reports and history when they are no longer needed.

Risk: Agent delivery rules may send HTML report attachments on messaging surfaces without per-run consent.

Mitigation: Require user approval before sharing reports outside the local terminal or session, and inspect report contents for sensitive workspace details before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danandbub/skills/driftwatch-oc)
- [BubBuilds homepage](https://bubbuilds.com)
- [Source-verified OpenClaw constants](references/constants.py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [JSON scan results, self-contained HTML reports, one-line check summaries, and human-facing Markdown or plain-text guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local OpenClaw workspace files; optional save and history modes persist scan history under ~/.driftwatch.]

## Skill Version(s):

1.1.4 (source: server release metadata; artifact constant reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
