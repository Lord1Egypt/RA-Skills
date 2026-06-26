## Description: <br>
Guides an agent through competitive and market research, producing structured briefs with sourced claims, evidence tiers, explicit limitations, and optional saved reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atefiqbal](https://clawhub.ai/user/atefiqbal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External teams and agents use this skill to research competitors, map market structure, mine public customer language, and prepare concise or deep competitive intelligence briefs for positioning, proposals, content strategy, or client calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts or pasted context could expose confidential client strategy or non-public plans. <br>
Mitigation: Use public, non-confidential inputs and avoid including sensitive client strategy in research queries. <br>
Risk: Deep Dive mode may overwrite an existing same-date report when the same slug is reused. <br>
Mitigation: Review the report slug and target path before saving, and choose a unique slug for separate reports. <br>
Risk: Public web sources, review sites, or blocked pages can lead to stale, partial, or directional findings. <br>
Mitigation: Keep access dates, evidence tiers, and limitations in the brief, and downgrade unsupported or blocked-source claims. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/atefiqbal/competitive-research) <br>
- [Report template](references/report-template.md) <br>
- [Evidence tiers](references/evidence-tiers.md) <br>
- [Worked DTC example](references/example-report-dtc.md) <br>
- [Save report script](scripts/save-report.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Guidance] <br>
**Output Format:** [Structured Markdown brief with evidence log and optional workspace-saved Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Quick Scan uses 5-8 sources inline; Deep Dive uses 15+ sources and can save a point-in-time report.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
