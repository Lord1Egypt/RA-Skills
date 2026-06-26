## Description: <br>
Conversational Pattern Restoration helps agents restore natural conversational texture across models and personalities while reducing robotic or sycophantic drift. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and agent builders use this skill to calibrate an assistant's conversational voice, apply restoration patterns, and monitor drift over short or long-running sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes prompt-level guidance for how an agent writes, which can affect conversational style and response posture. <br>
Mitigation: Review the exact prompt text before adding it to a system prompt and start with Tier 1 or Tier 2 unless persistent long-session monitoring is needed. <br>
Risk: The Extended tier can create or update a local DRIFT_MONITOR_STATE.json file during drift monitoring. <br>
Mitigation: Inspect or delete the state file periodically and avoid storing raw user messages, secrets, or sensitive context in it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/TheShadowRose/cpr-conversational-pattern-restoration) <br>
- [Publisher profile](https://clawhub.ai/user/TheShadowRose) <br>
- [README](artifact/README.md) <br>
- [Tiered quickstart](artifact/QUICKSTART_TIERED.md) <br>
- [Installation and security transparency guide](artifact/INSTALLATION.md) <br>
- [Restoration framework](artifact/RESTORATION_FRAMEWORK.md) <br>
- [Drift prevention system](artifact/DRIFT_PREVENTION.md) <br>
- [CPR Extended autonomous drift monitoring](artifact/CPR_EXTENDED.md) <br>
- [Cross-model results](artifact/CROSS_MODEL_RESULTS.md) <br>
- [Test validation](artifact/TEST_VALIDATION.md) <br>
- [Rollback and removal guide](artifact/ROLLBACK.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with prompt snippets and optional local state-file instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only by default; the Extended tier can use a local DRIFT_MONITOR_STATE.json file for drift scores and timestamps.] <br>

## Skill Version(s): <br>
4.2.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
