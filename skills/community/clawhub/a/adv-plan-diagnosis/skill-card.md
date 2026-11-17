## Description:

Diagnoses Ocean Engine and Tencent Ads advertising plans using an official Ocean Engine diagnosis API or Tencent Ads report data with a rule engine, then returns optimization guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suwangsen](https://clawhub.ai/user/suwangsen)

### License/Terms of Use:

MIT-0

## Use Case:

External advertisers, media buyers, and operations teams use this skill to diagnose under-delivery, high cost, and other campaign-plan performance issues for Ocean Engine and Tencent Ads. It gathers required platform and ad identifiers, runs the diagnosis script, and turns JSON results into a concise optimization report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads Ocean Engine and Tencent Ads API tokens from a local .env file and uses them to access advertising campaign data.

Mitigation: Keep the .env file restricted, use least-privilege and short-lived tokens, and rotate Tencent Ads tokens regularly.

Risk: The skill depends on external ad-platform APIs and unpinned Python dependencies, which can affect reliability or production reproducibility.

Mitigation: Pin dependencies, add request timeouts before production use, and monitor API errors returned by the diagnosis script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suwangsen/skills/adv-plan-diagnosis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with JSON-derived findings and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local ad-platform tokens and may return error JSON when required credentials or API calls fail.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence and skill definition)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
