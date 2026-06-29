## Description: <br>
Helps an agent correct availability-biased probability and risk estimates by identifying reference classes, checking base rates, diagnosing salience distortions, and documenting a corrected estimate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to evaluate claims about event frequency or risk that are driven by memorable examples, recent news, or personal anecdotes. It guides them to choose a reference class, retrieve base-rate evidence, diagnose availability distortions, and state decision implications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may rely on examples or uncited base rates for medical, legal, financial, safety, or other high-stakes decisions. <br>
Mitigation: Verify base-rate data and sources for the specific reference class before relying on the skill's output. <br>
Risk: A recent vivid event may be representative of a changed reference class, or the decision may warrant precautionary weight for rare catastrophic or irreversible outcomes. <br>
Mitigation: Check whether recent evidence is representative and preserve precautionary reasoning when the consequences justify it. <br>


## Reference(s): <br>
- [Primary sources for availability heuristic](references/sources.md) <br>
- [Method in Action: Tversky and Kahneman's 1973 Availability Studies](examples/tversky-and-kahnemans-1973-availability-studies.md) <br>
- [ClawHub skill page](https://clawhub.ai/deciqai/skills/availability-heuristic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with a structured availability-correction template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution; may recommend consulting external base-rate sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
