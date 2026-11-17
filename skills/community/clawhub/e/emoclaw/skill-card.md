## Description:

Give your AI emotions that grow from its own memories. Emoclaw builds a unique emotional state that shifts with every conversation, decays between sessions, and evolves over time through self-calibration. Train it on your agent's identity files and watch it develop its own emotional fingerprint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fenrirlabsnl](https://clawhub.ai/user/fenrirlabsnl)

### License/Terms of Use:


## Use Case:

Developers and agent builders use EmoClaw to add a persistent, configurable emotional-state layer to an AI agent, including setup, training, state injection, daemon operation, and calibration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can replace an existing project-level pyproject.toml.

Mitigation: Install in a disposable or backed-up project and review setup behavior before running it in an active workspace.

Risk: Configured identity or memory files may contain sensitive text that could be extracted and later sent to Anthropic during optional labeling.

Mitigation: Review bootstrap.source_files and memory_patterns, inspect extracted_passages.jsonl, and avoid --yes unless automated labeling is intentional.

Risk: Training resume can load PyTorch checkpoint files.

Mitigation: Resume training only from checkpoints created in a trusted local environment.

Risk: The daemon exposes a local Unix socket for state queries and message processing.

Mitigation: Run the daemon as a normal user, avoid root, and keep socket permissions and path configuration restricted to the intended user or group.

Risk: Dependencies are specified as version ranges without a reviewed lockfile.

Mitigation: Use pinned dependencies or a reviewed lockfile before deployment.

## Reference(s):

- [Model Architecture](artifact/references/architecture.md)
- [Calibration Guide](artifact/references/calibration-guide.md)
- [Configuration Reference](artifact/references/config-reference.md)
- [Emotion Dimensions](artifact/references/dimensions.md)
- [Upgrading](artifact/references/upgrading.md)
- [ClawHub Skill Page](https://clawhub.ai/fenrirlabsnl/skills/emoclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, JSON socket messages, YAML configuration, and an [EMOTIONAL STATE] text block.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local file paths, environment variable names, daemon commands, and generated emotional-state text for system prompt injection.]

## Skill Version(s):

1.0.6 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
