## Description:

Conversational Pattern Restoration helps agents restore natural conversational texture across models and personality styles while reducing robotic tone, sycophancy, and hype drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers, agent builders, and advanced agent users use this skill to define a conversational baseline, apply restoration patterns, and monitor drift in single-agent, single-user assistant workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change an agent's response style and may silently remove or rewrite parts of responses through drift checks.

Mitigation: Install only when a persistent voice/style layer is desired, review the prompt blocks before use, and add a guardrail that user requests, safety guidance, factual completeness, code, JSON, and compliance text must not be silently removed.

Risk: Extended mode may create and update a local DRIFT_MONITOR_STATE.json file for drift scores and action labels.

Mitigation: Start with Tier 1 or Core before enabling Extended mode, avoid Extended in shared or sensitive workspaces unless local state is acceptable, and inspect or delete DRIFT_MONITOR_STATE.json as needed.

## Reference(s):

- [README](artifact/README.md)
- [Tiered Quickstart](artifact/QUICKSTART_TIERED.md)
- [Installation and Security Transparency Guide](artifact/INSTALLATION.md)
- [Baseline Definition Template](artifact/BASELINE_TEMPLATE.md)
- [Restoration Framework](artifact/RESTORATION_FRAMEWORK.md)
- [Drift Prevention System](artifact/DRIFT_PREVENTION.md)
- [Model Calibration](artifact/MODEL_CALIBRATION.md)
- [Game Theory Integration](artifact/CPR_V4_GAME_THEORY.md)
- [CPR Extended](artifact/CPR_EXTENDED.md)
- [Cross-Model Results](artifact/CROSS_MODEL_RESULTS.md)
- [Practical Validation Testing](artifact/TEST_VALIDATION.md)
- [Rollback and Removal Guide](artifact/ROLLBACK.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with prompt blocks, checklists, examples, and optional local state-file instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, network access, credentials, or telemetry are required; Extended mode may guide an agent to maintain a local drift-monitor state file.]

## Skill Version(s):

4.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
