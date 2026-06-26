## Description: <br>
Fast Fact-Check guides an agent to answer factual questions quickly with bounded parallel web search, citation-backed evidence, and calibrated confidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentjiang06](https://clawhub.ai/user/vincentjiang06) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill when they need a quick, source-backed answer to a factual question or claim without requesting an exhaustive research report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fact-check requests can trigger external web queries that expose the user's query text to search providers or fetched sites. <br>
Mitigation: Avoid submitting confidential or sensitive material, or redact it before using the skill. <br>
Risk: The optional validator checks answer structure and citation resolution, but it does not prove that cited sources semantically support each claim. <br>
Mitigation: Review cited sources for actual claim support before relying on high-impact answers. <br>
Risk: The skill is optimized for speed, so it may stop after meeting its source bar rather than exhaustively surveying all available evidence. <br>
Mitigation: Use a deeper research workflow when the decision requires comprehensive coverage or formal due diligence. <br>


## Reference(s): <br>
- [Fast Fact-Check ClawHub listing](https://clawhub.ai/vincentjiang06/fast-fact-check) <br>
- [Skill instructions](SKILL.md) <br>
- [Search protocol](rules/search-protocol.md) <br>
- [Output contract](rules/output-contract.md) <br>
- [Source reliability and freshness](references/source-reliability.md) <br>
- [Metrics](references/metrics.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown BLUF answer with citations, confidence, tier, sources, and optional caveats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Time-boxed simple and complex tiers; optional Node.js structural validation for saved Markdown answers.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and CHANGELOG, released 2026-06-04) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
