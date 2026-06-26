## Description: <br>
Geopolitical conflict analysis for war sentiment assessment. Use when analyzing armed conflicts, military interventions, or regional crises to determine conflict duration probability, economic and commodity impacts, trading opportunities, and termination scenarios. Triggered by news article URLs about wars or military operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rafimchmd](https://clawhub.ai/user/rafimchmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to assess public news about armed conflicts, military interventions, or regional crises for duration probabilities, economic and commodity impacts, trading considerations, and likely termination scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-provided public news URLs, which could expose sensitive private, intranet, tokenized, or tracking links if supplied by mistake. <br>
Mitigation: Use only public news article URLs and remove private paths, tokens, and sensitive tracking parameters before invoking the skill. <br>
Risk: Geopolitical probabilities and commodity trading commentary may be incomplete, outdated, or unsuitable as a sole basis for decisions. <br>
Mitigation: Treat the output as one analytical perspective and verify important claims, probabilities, and trading implications with authoritative sources before acting. <br>


## Reference(s): <br>
- [Geopolitical Analysis Frameworks](references/frameworks.md) <br>
- [ClawHub skill page](https://clawhub.ai/rafimchmd/geopolitics-expert) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown analysis with five sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes conflict-duration probabilities, commodity and economic impact, trading odds, and ranked termination scenarios.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
