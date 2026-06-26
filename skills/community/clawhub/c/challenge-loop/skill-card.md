## Description: <br>
Challenge Loop adds adversarial hardening to judgment-containing agent outputs through inline self-refutation or an independent challenger subagent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enzowyf](https://clawhub.ai/user/enzowyf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add critical review to recommendations, plans, and other judgment-based outputs before relying on them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad challenge triggers may alter ordinary agent responses or start review behavior when the user did not clearly ask for it. <br>
Mitigation: Use the skill with explicit challenge commands and narrow activation rules for environments where unsolicited critique would be disruptive. <br>
Risk: Subagent challenge mode may add cost, latency, or repeated critique loops. <br>
Mitigation: Use inline mode for quick checks, keep configured round limits, and fall back to inline review if subagent spawning fails or times out. <br>


## Reference(s): <br>
- [Challenge Loop on ClawHub](https://clawhub.ai/enzowyf/challenge-loop) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review notes, revised content, and challenge summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Inline mode appends structured self-refutation; subagent mode may produce challenge findings followed by revised output.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog released 2026-04-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
