## Description:

Run a pre-publish monetization risk check for creator content across short-video platforms. Use when the user asks if a script is safe to monetize, wants policy-risk triage, needs advertiser-friendliness checks, or wants rewrite guidance to reduce demonetization and distribution risk.

This skill is for research and development only.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

External creators and creator-operations teams use this skill before publishing scripts, captions, hooks, thumbnails, or product-claim language to identify monetization, distribution, advertiser-safety, originality, and misleading-claim risks. It returns a green, yellow, or red verdict with mitigation edits and safer rewrite suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The assessment could be mistaken for a guarantee that a platform will monetize or distribute the content.

Mitigation: Present the result as policy-risk guidance and recommend final review against current platform policies before publishing.

Risk: Rewrite guidance could be misused to evade platform policy enforcement.

Mitigation: Keep edits focused on safety, clarity, advertiser suitability, and compliance, and do not provide policy-evasion tactics.

Risk: Commercial use may conflict with the artifact's stated non-commercial license terms.

Mitigation: Confirm the authoritative license terms and obtain separate commercial permission before commercial deployment.

## Reference(s):

- [Risk Scorecard](references/risk-scorecard.md)
- [ClawHub Skill Page](https://clawhub.ai/leooooooow/skills/creator-monetization-risk-checker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown risk audit with verdict, category scores, mitigation edits, and optional revised copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes green/yellow/red verdicts, confidence levels, top fixes, and safer rewrite suggestions when possible.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
