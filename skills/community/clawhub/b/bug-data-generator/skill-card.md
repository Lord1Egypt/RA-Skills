## Description: <br>
Generates a tool name and reviewable user-instruction list from a smart-home bug description, then can use the confirmed instructions to produce JSONL training data through data-generator. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HuaiBuer](https://clawhub.ai/user/HuaiBuer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data builders use this skill to turn smart-home assistant bug reports into candidate tool calls, user instruction variants, and JSONL training examples after human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated smart-home training examples may include real household, device, or scene names if supplied by the user. <br>
Mitigation: Use synthetic or anonymized device and scene names unless real household data is explicitly approved for training use. <br>
Risk: Incorrect generated instruction lists could produce misleading JSONL training data. <br>
Mitigation: Review and edit generated instruction lists before confirming JSONL generation. <br>
Risk: The skill can write generated instruction or JSONL files to user-selected paths and may depend on a companion data-generator skill. <br>
Mitigation: Choose output paths deliberately and verify the companion data-generator skill is trusted before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HuaiBuer/bug-data-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Text and JSON/JSONL examples with optional local output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reviewable instruction lists before JSONL generation; file output paths should be chosen deliberately.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
