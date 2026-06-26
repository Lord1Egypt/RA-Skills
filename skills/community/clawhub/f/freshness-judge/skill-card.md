## Description: <br>
Freshness Judge classifies normalized evidence as current, background, stale, undated, or malformed against a canonical time window to reduce the risk of treating old material as current. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z1one0415](https://clawhub.ai/user/z1one0415) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill after evidence normalization to separate current evidence from background, stale, undated, or malformed material for time-sensitive news, policy, market, and research tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compensation queries can increase search cost, external network use, or privacy exposure if run automatically. <br>
Mitigation: Cap extra searches and require review before running required or recommended compensation queries in sensitive workflows. <br>
Risk: Freshness classifications may be mistaken for final conclusions about the underlying evidence. <br>
Mitigation: Use the classifications as time-context signals and keep downstream review responsible for final factual judgments. <br>


## Reference(s): <br>
- [Freshness Judge ClawHub Page](https://clawhub.ai/z1one0415/freshness-judge) <br>
- [Freshness Rules](references/freshness-rules.md) <br>
- [Time Window Examples](references/time-window-examples.md) <br>
- [Freshness Judgment Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, json, guidance] <br>
**Output Format:** [JSON object with evidence freshness buckets, a freshness profile, risk flags, and optional compensation queries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; compensation queries are proposals for an orchestrator to review or run under budget and privacy controls.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
