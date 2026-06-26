## Description: <br>
Consilium helps users convene 3-5 configured AI models from different providers to analyze complex questions independently and synthesize consensus, disagreements, action items, and minority opinions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morozsm](https://clawhub.ai/user/morozsm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and decision-makers use Consilium to run multi-model deliberation on complex decisions, technical architecture, strategy, or other hard questions and receive a synthesized council report with action items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Council questions are sent to several configured model providers. <br>
Mitigation: Use only trusted providers and avoid secrets, private business details, or highly sensitive legal, medical, or financial information unless the provider set and session-retention settings are acceptable. <br>
Risk: Multi-model synthesis can still produce incorrect, incomplete, or overconfident guidance, especially for high-stakes decisions. <br>
Mitigation: Treat the council output as advisory, preserve minority views, and require human review before acting on legal, medical, financial, security, or business-critical recommendations. <br>
Risk: Each run uses multiple model calls, and an optional debate round can double the number of calls. <br>
Mitigation: Choose the fast, balanced, or thorough profile deliberately, set quorum and timeout values, and use debate rounds only when the additional cost is justified. <br>
Risk: If the orchestrator model is also a panelist, synthesis may favor that model's response. <br>
Mitigation: Randomize position order, quote specific panelist arguments with attribution, and explicitly preserve dissenting and minority opinions. <br>


## Reference(s): <br>
- [Council Protocol Details](references/PROTOCOL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown synthesis with optional JSON panel configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces consensus, disagreements, minority opinions, and prioritized action items; may create council-panel.json with model names and slot assignments.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
