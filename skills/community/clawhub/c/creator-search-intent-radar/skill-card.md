## Description: <br>
Converts TikTok, YouTube, and Instagram search and trend signals into a prioritized weekly content backlog with script angles and hook directions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Leooooooow](https://clawhub.ai/user/Leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and small content teams use this skill to turn social search, trend, comment, and FAQ signals into ranked topic decisions, hooks, CTAs, and a lightweight 7-day schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fallback-mode recommendations may be mistaken for live external trends. <br>
Mitigation: Require outputs to clearly label fallback mode and avoid treating recommendations as live trends unless they include provenance and capture times. <br>
Risk: Trend-signal collection can produce misleading content priorities if sources are weak or synthetic. <br>
Mitigation: Review source type, source link, capture time, and confidence before using the backlog for publishing decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Leooooooow/creator-search-intent-radar) <br>
- [Scoring Template](artifact/references/scoring-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown topic backlog with ranked entries, content angles, hook directions, CTAs, confidence labels, and a 7-day schedule] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses per-topic confidence labels and requires provenance fields when live demand signals are used.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
