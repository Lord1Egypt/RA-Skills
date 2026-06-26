## Description: <br>
Apply abductive reasoning to infer the best explanation from available observations, such as symptoms, clues, data points, or debugging signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanikua](https://clawhub.ai/user/wanikua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other external users use this skill to catalog observations, generate candidate explanations, compare explanatory power, and identify tests that could distinguish the leading hypotheses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad diagnostic-style reasoning can produce plausible but incorrect explanations in high-stakes domains. <br>
Mitigation: Keep the analysis bounded, require domain-specific safeguards, and have qualified reviewers validate conclusions before acting on medical, legal, financial, security, or other high-stakes output. <br>
Risk: Hypothesis generation may overfit limited or unreliable observations. <br>
Mitigation: Ask the agent to label observation reliability, state assumptions, identify falsifying evidence, and propose tests that distinguish the leading explanations. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown structured as observations, hypothesis comparisons, rankings, stress tests, and next steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution, credential use, data access, persistence, or destructive behavior is indicated by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
