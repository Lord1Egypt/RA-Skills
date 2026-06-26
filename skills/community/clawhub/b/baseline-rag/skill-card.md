## Description: <br>
Extracts and checks factual claims with web sources, scores baseline confidence around 50-70%, and flags claims that need higher verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crftsmnd](https://clawhub.ai/user/crftsmnd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to fact-check claims from prompts by searching web sources, comparing supporting and rejecting evidence, and returning a confidence-scored recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confidence scores are heuristic and may be mistaken for statistically rigorous verification. <br>
Mitigation: Treat scores as rough guidance, review cited sources, and avoid relying on the skill as the sole authority for high-stakes claims. <br>
Risk: The skill can activate on broad verification wording and may process sensitive claims through web search or an external endpoint. <br>
Mitigation: Use it for non-sensitive claims, review the external endpoint before use, and avoid sending private or regulated information. <br>
Risk: External verification or upsell links may steer users outside the skill. <br>
Mitigation: Review external services and pricing before following links or sharing information. <br>


## Reference(s): <br>
- [ClawHub Baseline-RAG listing](https://clawhub.ai/crftsmnd/baseline-rag) <br>
- [Baseline-RAG endpoint](https://omni-skills.cvapi.workers.dev/skill/baseline-rag) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with source list, confidence table, and recommendation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes heuristic confidence ranges and source citations; scores are not rigorous statistical measurements.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
