## Description:

Build and debug browser keyboard testers and physical-key handling, covering KeyboardEvent.code vs key, keys the browser never sees, rollover and ghosting, key chatter, rapid trigger tap tests and SOCD / Snap Tap detection. Use when writing code that tracks which physical keys are held, a keyboard tester page, or keyboard input for games in the browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hlplanet](https://clawhub.ai/user/hlplanet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building browser keyboard testers or game input handling use this skill to track physical keys and interpret keyboard events, rollover, chatter, rapid trigger taps, and SOCD behavior. It also explains what browser input cannot measure reliably.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security scan coverage is partial because several local path-like references could not be resolved.

Mitigation: Review referenced local resources before relying on the skill guidance or installing it.

Risk: Browser event timing is coarsened and operating systems batch input, so timing figures can be mistaken for precise latency or polling measurements.

Mitigation: Label timing figures as estimates, report gaps to at most 0.1 ms, and do not claim they measure keyboard latency or polling rate.

Risk: A browser tester cannot distinguish a keyboard rollover limit from ghosting when a held key is not reported.

Mitigation: Explain that the result reflects keys reported by the operating system and cannot identify which hardware behavior suppressed a key.

## Reference(s):

- [HLPlanet Online Keyboard Tester](https://www.hlplanet.com/online-keyboard-tester-tool/)
- [Rapid Trigger & SOCD Tester reference](https://github.com/hlplanet/rt-socd-tester)
- [ClawHub skill release](https://clawhub.ai/hlplanet/skills/browser-keyboard-testing)

## Skill Output:

**Output Type(s):** [Code, Guidance]

**Output Format:** [Markdown with JavaScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes browser input and timing limitations.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
