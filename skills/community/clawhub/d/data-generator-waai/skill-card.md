## Description: <br>
Data Generator creates JSONL training data from a tool name and a list of user commands by calling a configured LLM endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HuaiBuer](https://clawhub.ai/user/HuaiBuer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data builders use this skill to batch-generate tool-call training samples from natural-language commands and write them as JSONL for downstream model training or testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command text and generated prompts may be sent to the configured model service. <br>
Mitigation: Use only a trusted API_URL or base_url and avoid putting secrets, private data, or sensitive user content in command text. <br>
Risk: The documented Excel and custom-prompt examples do not match the current Python interface. <br>
Mitigation: Use the current Generator.generate(tool_name, commands, output_file) interface or the CLI form shown by data_generator.py. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HuaiBuer/data-generator-waai) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/HuaiBuer) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python API or CLI output that writes JSONL training records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a trusted LLM endpoint configured through API_URL or constructor parameters.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; SKILL.md frontmatter says 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
