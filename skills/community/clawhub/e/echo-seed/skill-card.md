## Description: <br>
A simple and elegant idea capture tool for quick notes, smart categorization, timeline views, optional AI analysis, and multi-platform sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zheznanohana](https://clawhub.ai/user/zheznanohana) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and personal-productivity users use Echo Seed to run a local idea and note capture app with web entry, Telegram input, optional AI analysis, and optional Notion or Google Calendar synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notes and links can be sent to external AI, Notion, Calendar, or Telegram-related services with weak scoping and unsafe defaults. <br>
Mitigation: Run the app behind localhost-only access or authentication, avoid sensitive notes and internal URLs, and keep sync features disabled until credentials and opt-in controls are reviewed. <br>
Risk: Untrusted URL analysis may fetch content before URL-handling protections are hardened. <br>
Mitigation: Do not analyze untrusted links until URL fetching is fixed and reviewed for safe network boundaries. <br>


## Reference(s): <br>
- [Echo Seed ClawHub release](https://clawhub.ai/zheznanohana/echo-seed) <br>
- [README](README.md) <br>
- [AI feature documentation](README-AI.md) <br>
- [Configuration example](config.example.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, and Python and HTML source files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and installs Flask and Requests; optional API credentials enable AI, Notion, Google Calendar, and Telegram integrations.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
