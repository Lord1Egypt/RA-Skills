## Description:

ESP-IDF expert skill for environment checks, example discovery, GPIO safety review, build diagnostics, panic decoding, monitor analysis, flashing, and component lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[movecall](https://clawhub.ai/user/movecall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect ESP-IDF environments, navigate examples, audit ESP32-family GPIO choices, diagnose builds and monitor logs, decode panics, and generate reviewable component or partition suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read ESP-IDF project files and local examples during diagnostics.

Mitigation: Use it only on intended project directories and review file paths surfaced in results.

Risk: Build, flash, and monitor tools can run idf.py against connected hardware when invoked.

Mitigation: Confirm the project path, chip target, serial port, and ESP-IDF environment before invoking execution tools.

Risk: Component lookup contacts the official Espressif component registry and may return dependency snippets or patch-style suggestions.

Mitigation: Review registry results, dependency snippets, and manifest changes before applying them to a project.

Risk: Generated shell-command suggestions may be inappropriate for a specific workstation or project state.

Mitigation: Treat commands as proposals and review them before running.

## Reference(s):

- [Claw ESP Expert skill page](https://clawhub.ai/movecall/skills/claw-esp-expert)
- [Publisher profile](https://clawhub.ai/user/movecall)
- [Espressif ESP-IDF repository](https://github.com/espressif/esp-idf.git)
- [Espressif ESP-IDF Gitee mirror](https://gitee.com/EspressifSystems/esp-idf.git)
- [Espressif GitHub assets mirror](https://dl.espressif.cn/github_assets)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON tool results and Markdown guidance with shell command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Patch-style before/after suggestions may be returned for partition tables or component manifests; generated dependency and command suggestions should be reviewed before use.]

## Skill Version(s):

0.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
