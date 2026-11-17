## Description:

Run deep research queries using Chonkie DeepResearch and return comprehensive research reports with citations for market analysis, competitive intelligence, technical deep dives, and other research-heavy tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chonknick](https://clawhub.ai/user/chonknick)

### License/Terms of Use:


## Use Case:

Developers, analysts, and external users use this skill to launch Chonkie DeepResearch jobs from an agent, retrieve cited reports, and answer follow-up questions against saved report files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research prompts and related context are sent to Chonkie through the chdr CLI.

Mitigation: Avoid secrets and regulated data in research queries, and store CHONKIE_API_KEY securely.

Risk: The setup instructions use mutable chdr and Rust installation commands.

Mitigation: Prefer a pinned and verified chdr/Rust installation path before deploying the skill.

Risk: The skill describes recurring cron monitoring for research status checks.

Mitigation: Do not create the suggested cron job unless cleanup, scope, and explicit approval are defined.

Risk: Generated research reports can be very large.

Mitigation: Use targeted search and bounded reads when answering follow-up questions about saved reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chonknick/skills/chonkie-deepresearch)
- [Chonkie](https://chonkie.ai)
- [Chonkie API keys](https://labs.chonkie.ai/settings/api-keys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples; research results are saved as JSON and Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research runs can take 2-10 minutes; reports may be very large, so the skill instructs agents to read targeted sections instead of loading full report files.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
