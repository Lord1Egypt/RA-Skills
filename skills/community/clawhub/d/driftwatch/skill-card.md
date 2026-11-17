## Description:

DriftWatch monitors agent identity drift in OpenClaw workspaces by using git history to detect changes to identity, operating-rule, tool, user, and memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m-maciver](https://clawhub.ai/user/m-maciver)

### License/Terms of Use:


## Use Case:

Developers and agent operators use DriftWatch to audit whether agent identity files have changed over time and to identify changes that may need human review before the next agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default LLM analysis can send sensitive identity and memory diff snippets to Claude.

Mitigation: Use --no-llm for local-only scans, and avoid cron mode unless sharing those snippets with Claude is acceptable.

Risk: The tool writes drift reports even though the documentation describes it as read-only.

Mitigation: Run it only where report file creation is acceptable, and set --output to a controlled path for scheduled use.

Risk: Generated approval and confidence labels are advisory and may not prove human review.

Mitigation: Manually review flagged, high-impact, or unexplained identity changes before relying on the report.

## Reference(s):

- [DriftWatch README](artifact/README.md)
- [ClawHub Skill Page](https://clawhub.ai/m-maciver/skills/driftwatch)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown report with terminal summary text and optional JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default analysis may invoke Claude unless --no-llm is used; reports are written to the skill directory or a requested output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
