## Description: <br>
Give your AI emotions that grow from its own memories. Emoclaw builds a unique emotional state that shifts with every conversation, decays between sessions, and evolves over time through self-calibration. Train it on your agent's identity files and watch it develop its own emotional fingerprint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fenrirlabsnl](https://clawhub.ai/user/fenrirlabsnl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use EmoClaw to add a local, persistent emotional-state model to an AI agent, train it from identity and memory files, and inject a current emotional-state block into prompts or runtime flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can overwrite project-level build files and install broad Python dependencies. <br>
Mitigation: Review setup before running it, back up any existing pyproject.toml, use an isolated test repo where practical, and pin dependencies before installation. <br>
Risk: Configured identity or memory files may be extracted into local JSONL training data. <br>
Mitigation: Inspect emoclaw.yaml before extraction so only intended source files are included, then review emotion_model/data before further processing. <br>
Risk: Optional API labeling can send extracted passages to an external service. <br>
Mitigation: Use API labeling only after reviewing the extracted data and confirming that ANTHROPIC_API_KEY-based labeling is intended. <br>
Risk: Derived emotional profile data and source passages may remain on disk. <br>
Mitigation: Delete memory/emotional-state.json and extracted JSONL files when the derived profile or source passages should not be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fenrirlabsnl/emoclaw) <br>
- [Model Architecture](references/architecture.md) <br>
- [Configuration Reference](references/config-reference.md) <br>
- [Emotion Dimensions](references/dimensions.md) <br>
- [Calibration Guide](references/calibration-guide.md) <br>
- [Upgrading the Emotion Skill](references/upgrading.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python examples, YAML configuration, JSON daemon messages, and emotional-state text blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include local files such as emotion_model/data JSONL files, model checkpoints, and memory/emotional-state.json when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
