## Description:

Fast AI/ML conference deadline lookup and submission-window routing. Use when the user asks for AI conference deadlines, target venue timing, whether to submit to AAAI/ICLR/AISTATS/CLeaR/WSDM/ACL/EMNLP/NeurIPS/ICML/CVPR/etc., how to schedule a research sprint around deadlines, or which venue is urgent for a paper candidate. Start from high-quality deadline radar sources, then verify decision-critical dates against official CFP/OpenReview/submission pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1587causalai](https://clawhub.ai/user/1587causalai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research managers use this skill to find AI/ML conference deadline windows, verify decision-critical dates against official CFP/OpenReview/submission pages, and turn venue timing into concise sprint or submission recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper uses a predictable temporary cache path that could corrupt user-writable files on shared machines.

Mitigation: Review before installing on shared machines; run the helper with --no-cache or set AI_CONFERENCE_DEADLINE_RADAR_CACHE to a private user-controlled path.

Risk: Radar and index pages can lag official CFP, OpenReview, or submission pages and may mislead submission decisions.

Mitigation: Use radar sources only for discovery and verify decision-critical deadlines against official sources before labeling dates official_confirmed.

## Reference(s):

- [Source policy for AI conference deadlines](references/source-policy.md)
- [ClawHub skill page](https://clawhub.ai/1587causalai/skills/ai-conference-deadline-radar)
- [mlciv AI deadlines](https://mlciv.com/ai-deadlines/?sub=ML,CV,CG,NLP,RO,SP,DM,AP,KR,HCI,EDU)
- [CCFDDL conference deadline RSS](https://ccfddl.com/conference/deadlines_zh.xml)
- [AI Deadlines](https://aideadlines.org/)
- [aideadlin.es](https://aideadlin.es/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with concise deadline tables, source-status labels, verification notes, and optional inline shell commands for the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve official_confirmed, historical_estimate, radar_hint, and unverified labels; decision-critical dates require official-source verification.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
