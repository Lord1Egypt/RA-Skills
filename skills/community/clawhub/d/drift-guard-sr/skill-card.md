## Description:

Detect personality drift, sycophancy creep, and capability degradation in AI agents before they become problems. Tracks behavior metrics over time against healthy baselines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Drift Guard to capture healthy behavior baselines, monitor agent responses for measurable drift, and generate trend reports that support review and recovery decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool reads local agent response files and writes baseline, history, alert, and log files.

Mitigation: Run it in a workspace where those local files are expected, and avoid pointing it at sensitive response logs unless local storage is acceptable.

Risk: Using --config imports a Python configuration file as executable code.

Mitigation: Use only trusted config files and review custom configuration before execution.

Risk: Drift history retention is not enforced in the inspected code.

Mitigation: Monitor, rotate, or prune drift_history.json during long-running use.

Risk: Pattern-based drift metrics can produce false positives and do not explain root cause.

Mitigation: Treat alerts as review signals, correlate them with activity logs, and keep remediation as a separate human-approved step.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/theshadowrose/skills/drift-guard-sr)
- [README](artifact/README.md)
- [Limitations](artifact/LIMITATIONS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; included scripts produce local JSON and text reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external dependencies; analyzes local text responses and writes local baseline, history, alert, and report files.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
