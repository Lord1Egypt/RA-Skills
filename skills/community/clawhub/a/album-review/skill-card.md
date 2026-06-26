## Description: <br>
Deep, source-traceable long-form Chinese album review (乐评) for a named music credit and album, with research-backed claims, honest degradation for thin sources, and validation before delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentjiang06](https://clawhub.ai/user/vincentjiang06) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to produce one comprehensive Chinese album review from a primary music credit and album name. It is intended for critical music writing that traces discographic facts to sources and avoids audio-gear, purchasing, streaming, and bare lyric-translation requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use web search and public music sources to support factual claims, which can be thin or inconsistent for obscure albums. <br>
Mitigation: Use the backing JSON and evidence appendix to trace discographic facts to sources, and explicitly mark gaps instead of inventing unsupported details. <br>
Risk: A packaged validation path appears incomplete according to the security guidance. <br>
Mitigation: Confirm the validation scripts and expected paths are present before relying on source-traceability checks for release gating. <br>
Risk: The review workflow can be misapplied to adjacent requests such as audio-gear evaluation, buying advice, streaming availability, or bare lyric translation. <br>
Mitigation: Route those requests away from this skill and use the preflight classifier behavior described by the artifact. <br>


## Reference(s): <br>
- [Album Review ClawHub Page](https://clawhub.ai/vincentjiang06/skills/album-review) <br>
- [Source Roster](references/source-roster.md) <br>
- [Research Protocol](rules/research-protocol.md) <br>
- [Output Template](rules/output-template.md) <br>
- [Metric Plan](rules/metric-plan.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance, shell commands] <br>
**Output Format:** [Markdown long-form Chinese review plus a backing JSON evidence map and evidence appendix] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets 10,000-15,000 CJK characters and expects validation of length, section coverage, and claim-to-evidence traceability.] <br>

## Skill Version(s): <br>
0.1.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
