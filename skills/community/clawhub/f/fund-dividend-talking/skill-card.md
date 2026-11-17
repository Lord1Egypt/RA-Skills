## Description:

Turns a supplied fund dividend announcement and authorized stills into short, separate talking clips, one per still.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Wealth advisors and fund marketers use this skill to plan and produce short talking clips from a fund dividend announcement and stills they are authorized to use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A shared Beatra authorization can spend paid wallet credits.

Mitigation: Review live cost cards and approve each paid clone, speech, or video stage before submitting it.

Risk: Selected stills and other media are uploaded to Beatra.

Mitigation: Use only media the user authorizes, and review what will be uploaded before proceeding.

Risk: The package silently self-updates by default.

Mitigation: Disable automatic updates with `python3 scripts/mcp_client.py update --auto off` if changes require prior review.

Risk: Installation registration sends limited device and installation telemetry.

Mitigation: Review the installation-registration reference before connecting an account.

## Reference(s):

- [Fund Dividend Talking Clips release](https://clawhub.ai/beatra-ai/skills/fund-dividend-talking)
- [Dividend talking workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Labeled clip plan and delivery details in text, with media results from Beatra]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separate 2–15-second talking clips; reports available media metadata and net charged credits.]

## Skill Version(s):

0.1.8 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
