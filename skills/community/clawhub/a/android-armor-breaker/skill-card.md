## Description:

Android Armor Breaker helps agents guide authorized Android APK protection analysis, Frida-based dynamic unpacking, root memory extraction, anti-debug bypass workflows, and DEX extraction for security research and testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haonings](https://clawhub.ai/user/haonings)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, mobile security engineers, and authorized security testers use this skill to analyze Android APK protections, choose an unpacking strategy, run Frida or root-memory extraction tooling, and handle extracted DEX artifacts responsibly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use root and Frida to bypass Android application protections, read process memory, and extract code or data.

Mitigation: Use only on apps and devices the operator owns or has written permission to assess, and run in an isolated rooted test device or emulator.

Risk: Extracted DEX files, reports, logs, and memory dumps may contain sensitive application code, tokens, keys, or user data.

Mitigation: Treat all extracted artifacts as sensitive data, restrict access, avoid redistribution without authorization, and delete test outputs when no longer needed.

Risk: Dependency and device tooling such as Frida, ADB, and Python packages can affect the trust boundary of the test environment.

Mitigation: Review bundled scripts before execution, install dependencies from trusted sources, and pin or verify dependency versions before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haonings/skills/android-armor-breaker)
- [Security and Responsible Use Guidelines](artifact/SECURITY.md)
- [Android Armor Breaker README](artifact/README.md)
- [Quick Start Guide](artifact/QUICK_START.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, analysis]

**Output Format:** [Markdown guidance with inline shell commands and references to generated files such as DEX files, JSON reports, and execution logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or reference sensitive Android memory dumps, extracted DEX files, analysis reports, and local logs during authorized testing.]

## Skill Version(s):

2.2.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
