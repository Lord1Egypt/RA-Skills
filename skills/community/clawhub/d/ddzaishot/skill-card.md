## Description:

Ddzaishot helps users analyze Dou Dizhu games by recognizing on-screen cards, tracking play history, and suggesting moves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bladezhang](https://clawhub.ai/user/bladezhang)

### License/Terms of Use:

MIT-0

## Use Case:

Players or developers running a local Dou Dizhu assistant use this skill to scan a visible game screen, keep card counts, request AI move suggestions, and optionally automate calibrated card-play clicks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full-screen capture can expose sensitive information outside the game window.

Mitigation: Close sensitive windows before scanning and delete saved screenshots in logs after use.

Risk: Mouse automation can click the wrong target if calibration is stale or the active window changes.

Mitigation: Use automatic play only after calibration and only while the intended game window is active.

Risk: Unpinned dependency ranges can change behavior across installations.

Mitigation: Install in a virtual environment and pin dependency versions for repeatable use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bladezhang/skills/ddzaishot)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Interactive terminal text and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save screenshots to logs and may issue calibrated mouse clicks when automatic play is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
