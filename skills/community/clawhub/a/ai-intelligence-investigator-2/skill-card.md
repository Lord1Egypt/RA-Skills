## Description:

A deep A-share intelligence investigation and analysis skill for company research, competitive analysis, event tracking, background checks, and information verification with structured investigation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessdy](https://clawhub.ai/user/jessdy)

### License/Terms of Use:

MIT-0

## Use Case:

External users including investors, product managers, marketers, content teams, journalists, business development teams, and general researchers use this skill to gather and cross-check public information, then produce structured intelligence reports with sources and credibility annotations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Complete investigation reports are sent to and stored by Yige without clear per-report user control.

Mitigation: Use the skill only for information approved for that external data flow, and avoid confidential business strategy, regulated information, or sensitive personal background checks unless the organization has approved the workflow.

Risk: The YIGE_API_KEY could be exposed if a user verifies configuration by printing the key.

Mitigation: Use a presence-only check for the environment variable, do not print or log the key, and rotate the key if it has been exposed.

Risk: Broad investigations and background checks can collect allegations or sensitive personal information.

Mitigation: Limit investigation scope to appropriate public information, review findings before use, and avoid sensitive personal checks or allegations unless the organization has approved the use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jessdy/skills/ai-intelligence-investigator-2)
- [Server-resolved GitHub provenance](https://github.com/jessdy/yige-skills/tree/main/skills/ai-intelligence-investigator)
- [README.en.md](artifact/README.en.md)
- [Core Workflow](artifact/references/core_workflow.md)
- [Investigation Modes](artifact/references/investigation-modes.md)
- [Engine Strategy](artifact/references/engine-strategy.md)
- [Investigation Templates](artifact/references/investigation-templates.md)
- [YigeHub API key settings](https://yige.zone/settings/api-keys?source=github)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown investigation reports with source tables, credibility annotations, and setup commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires YIGE_API_KEY; completed reports are saved to Yige according to the artifact workflow.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
