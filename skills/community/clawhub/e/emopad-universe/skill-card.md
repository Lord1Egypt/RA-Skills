## Description:

EmoPAD Universe helps users locate emotions in the Pleasure-Arousal-Dominance coordinate system and provides continuous real-time emoNebula monitoring with periodic emotion nebula chart popups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beardao](https://clawhub.ai/user/beardao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor biometric sensor signals, query current emotion PAD status, and generate emotion nebula visualizations for supported EEG, PPG, and GSR hardware. The PAD calculation is heuristic and is not described as personalized emotion recognition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for continuous local biometric and emotion monitoring.

Mitigation: Install only when this monitoring is intended, review the code first, and avoid running it with elevated privileges.

Risk: Local processes can query the emotion API on 127.0.0.1:8766.

Mitigation: Run in an isolated local environment and limit access to trusted local processes.

Risk: Stop and start behavior may terminate unrelated processes with matching command patterns.

Mitigation: Inspect running processes before using stop/start commands and prefer a contained environment for execution.

Risk: Installation can automatically install Python dependencies and start background monitoring services.

Mitigation: Pin dependencies or install them in an isolated environment before enabling auto-start behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beardao/skills/emopad-universe)
- [Bilibili demonstration video](https://www.bilibili.com/video/BV1QKPUz7EHV/?spm_id_from=333.337.search-card.all.click)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with command examples, configuration snippets, status text, JSON API responses, and PNG visualization output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can start a local FastAPI service on 127.0.0.1:8766 and generate periodic emotion nebula image snapshots.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
