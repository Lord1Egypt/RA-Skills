## Description: <br>
Classifies script inputs into Level -1 through 4 and extracts scene, character, dialogue, action-density, prop, costume, and risk-flag information for downstream editing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangliujiao-tal](https://clawhub.ai/user/huangliujiao-tal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and agent workflows use this skill to classify Chinese-language script material by readiness level and extract structured script elements before routing the work to downstream creative or consistency-checking skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Classification and extraction quality may be lower for non-Chinese or highly ambiguous script inputs. <br>
Mitigation: Verify the detected level, confidence, and evidence before using the result downstream; route low-confidence outputs for human review. <br>
Risk: Downstream workflows could treat a classification as permission to rewrite content. <br>
Mitigation: Use this skill as a read-only analysis step and preserve the original input until a separate editing skill is explicitly invoked. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangliujiao-tal/editor-classify-and-parse) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON object with concise explanatory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes detected level, confidence, evidence, extracted structure, and risk flags; no file writes, command execution, network access, or credential handling are requested by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
