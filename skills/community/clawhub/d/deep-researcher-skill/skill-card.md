## Description: <br>
Conducts structured, multi-source research across web, academic, video, forum, and optional API sources, then synthesizes cited findings into briefs, deep dives, comparisons, temporal updates, and decision matrices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geoffguides](https://clawhub.ai/user/geoffguides) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and developers use this skill to plan and execute comprehensive investigations, evaluate source quality, calibrate confidence, and produce actionable research outputs with citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to attempt paywall bypass by default, which may conflict with content access terms or organizational policy. <br>
Mitigation: Use only open, licensed, subscribed, or otherwise authorized sources, and require operators to skip or mark restricted sources as unverified when access is not permitted. <br>
Risk: Research workflows may involve optional API keys or external services. <br>
Mitigation: Provide credentials through the host platform's secret-management mechanism rather than plain chat or committed configuration files. <br>
Risk: Synthesized research can overstate confidence if sources are stale, low quality, or contradictory. <br>
Mitigation: Preserve source citations, confidence calibration, source-quality labels, and knowledge-gap notes in final outputs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/geoffguides/deep-researcher-skill) <br>
- [Publisher profile](https://clawhub.ai/user/geoffguides) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown research reports, tables, source lists, confidence notes, and optional JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are expected to include citations, confidence calibration, source-quality notes, and follow-up recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
