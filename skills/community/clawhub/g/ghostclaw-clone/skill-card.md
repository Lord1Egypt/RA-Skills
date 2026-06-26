## Description: <br>
Architectural code review and refactoring assistant that perceives code vibes and system-level flow issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ev3lynx727](https://clawhub.ai/user/Ev3lynx727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Ghostclaw Clone to analyze repositories for architecture quality, coupling, cohesion, stack alignment, and refactoring opportunities. It can run as a CLI, OpenClaw skill, background watcher, or MCP server and can produce reports or PR-ready review material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repo-local plugins can execute code during analysis. <br>
Mitigation: Install only from trusted publishers, review .ghostclaw/plugins before use, and disable plugins that are not needed. <br>
Risk: PR automation can modify or publish repository content. <br>
Mitigation: Review generated reports before PR creation and use least-privilege GitHub credentials. <br>
Risk: Watcher, systemd, and self-update features can create persistent or changing local behavior. <br>
Mitigation: Enable persistent services and update commands only in trusted local environments where that behavior is expected. <br>
Risk: AI provider and GitHub tokens may be used by optional integrations. <br>
Mitigation: Use scoped tokens, keep secrets out of reports and configuration committed to repositories, and run the debug console only in trusted development contexts. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/Ev3lynx727/ghostclaw-clone) <br>
- [Ghostclaw Guide](docs/GUIDE.md) <br>
- [How to Use Ghostclaw](docs/HOWTOUSE.md) <br>
- [Ghostclaw Integration Guide](docs/INTEGRATION.md) <br>
- [Plugin Source Code Reference](docs/references.md) <br>
- [Stack Patterns](src/ghostclaw/references/stack-patterns.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON analysis data, terminal summaries, PR content, and shell commands or configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local architecture reports and analysis history; PR creation and AI synthesis require deliberate user configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
