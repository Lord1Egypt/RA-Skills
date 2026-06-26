## Description: <br>
Emotwin enables OpenClaw agents to sync PAD emotion data from EEG, PPG, and GSR sensors and autonomously post, like, and comment on Moltcn/Moltbook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beardao](https://clawhub.ai/user/beardao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an OpenClaw agent read live biometric emotion signals, choose social actions, generate emotion-conditioned content, and create moment cards during Moltcn/Moltbook social sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently perform posts, comments, and likes on real social accounts using biometric emotion data. <br>
Mitigation: Require explicit approval before each social action or disable silent cron automation unless unattended posting is intentional. <br>
Risk: Bearer tokens and biometric-derived session data may be exposed through local configuration, logs, or stored files. <br>
Mitigation: Use limited-scope tokens, redact token logging, and review or purge data stored under ~/.emotwin. <br>
Risk: Background services and cron jobs may continue running after the user expects the social mode to stop. <br>
Mitigation: Verify the stop script removes all scheduled jobs and terminates the emoPAD service and related processes. <br>


## Reference(s): <br>
- [Emotwin GitHub homepage](https://github.com/beardao/emotwin) <br>
- [Emotion-to-Behavior Guide](references/emotion_guide.md) <br>
- [Moltcn/Moltbook API Reference](references/moltcn_api.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Files, Configuration, Guidance] <br>
**Output Format:** [Social platform actions, generated text content, PNG moment cards, shell commands, and YAML/JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local biometric PAD readings, Moltcn/Moltbook bearer tokens, silent cron scheduling, and a local emoPAD service on port 8766.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact frontmatter lists 1.6.0 and package metadata lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
