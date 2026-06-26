## Description: <br>
Analyzes changes in a primary requirements document against related documents and produces a structured impact report identifying synchronized changes, required updates, unaffected changes, and recommended priorities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaycchang025-droid](https://clawhub.ai/user/kaycchang025-droid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Requirements analysts, product teams, and documentation maintainers use this skill to compare a main requirements change source with related documents and decide exactly which documents need synchronized updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requirement documents may contain private business requirements or sensitive product details. <br>
Mitigation: Use the skill only with documents the agent is authorized to inspect, and specify the main document, change source, and related documents explicitly. <br>
Risk: Impact analysis can produce incorrect or over-broad update recommendations if the compared documents are incomplete or stale. <br>
Mitigation: Review the structured report before applying changes, especially items marked as needing synchronization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaycchang025-droid/generic-requirement-impact-check) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown report with lists and a summary table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports synchronized changes, changes requiring updates with priorities and revision advice, confirmed unaffected changes, and a final summary table.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
