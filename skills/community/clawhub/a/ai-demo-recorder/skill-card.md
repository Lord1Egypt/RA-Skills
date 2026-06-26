## Description: <br>
Records AI-driven browser demos with screencli, creating polished MP4 or GIF walkthroughs with visual effects and optional cloud upload. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leshems](https://clawhub.ai/user/leshems) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, product teams, and documentation authors use this skill to record browser-based demos, walkthroughs, before-and-after UI comparisons, and shareable product videos from an agent-driven prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse logged-in browser sessions when recording private applications. <br>
Mitigation: Use low-privilege test accounts, avoid recording secrets, and delete unused ~/.screencli/auth/ session files when no longer needed. <br>
Risk: Recordings upload to the screencli cloud service by default. <br>
Mitigation: Use --local for internal, customer, regulated, or sensitive demos, and install only if the external screencli CLI and cloud service are trusted. <br>


## Reference(s): <br>
- [CLI Reference](references/cli-reference.md) <br>
- [Effects Reference](references/effects.md) <br>
- [screencli website](https://screencli.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce local MP4 or GIF recordings and, unless local mode is used, shareable screencli.sh links.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact metadata.version is 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
