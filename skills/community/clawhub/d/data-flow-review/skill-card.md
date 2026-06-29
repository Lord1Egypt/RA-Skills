## Description: <br>
Reviews code by tracing data flow, state transitions, branch behavior, field semantics, and persistence consistency across related paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modeyapu](https://clawhub.ai/user/modeyapu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code reviewers use this skill to reconstruct end-to-end data flows during code review, audits, and patch checks. It helps identify stale state, unsafe persistence timing, branch regressions, payload provenance issues, and downstream contract breaks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides the agent to inspect relevant code paths, which may expose workspace code to the review session. <br>
Mitigation: Use it only in workspaces where agent code-reading for the requested review is acceptable. <br>


## Reference(s): <br>
- [data-flow-review on ClawHub](https://clawhub.ai/modeyapu/data-flow-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review findings and flow summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings-first output with severity, file references, triggering path or branch, and concrete data correctness risk.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
