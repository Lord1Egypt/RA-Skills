## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement for coding agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Adityasagar2](https://clawhub.ai/user/Adityasagar2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to capture corrections, command failures, feature requests, and recurring workflow discoveries so they can be reviewed and promoted into durable agent guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning capture can carry sensitive prompts, credentials, personal data, or confidential error output into future agent memory. <br>
Mitigation: Do not log raw secrets, tokens, personal data, full prompts, or confidential output; require human review before promoting entries into durable instruction files. <br>
Risk: Broad automatic hooks can add persistent agent-learning behavior across more sessions or projects than intended. <br>
Mitigation: Prefer project-local setup, avoid empty or global hook matchers, and scope hook activation to the workflows where learning capture is wanted. <br>


## Reference(s): <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Learning Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces learning-entry templates, hook setup guidance, and reminder text for agent sessions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
