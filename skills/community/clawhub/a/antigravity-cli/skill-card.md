## Description: <br>
Helps agents run, configure, troubleshoot, and explain Google Antigravity CLI (`agy`) across one-shot, TUI, artifact review, plugin, permissions, and migration workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wei840222](https://clawhub.ai/user/wei840222) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose and operate the `agy` command-line or TUI workflow, including safe permission settings, artifact review, configuration, and migration from Gemini CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides use of an agent CLI that can run commands, modify files, and interact with credentials or external tools. <br>
Mitigation: Keep sandboxing and permission prompts enabled by default, use review-oriented permission presets in unfamiliar repositories, and scope filesystem, URL, and MCP access narrowly. <br>
Risk: Options such as `--dangerously-skip-permissions` and settings such as `always-proceed` can bypass normal review. <br>
Mitigation: Use those modes only in trusted, low-risk workspaces when explicitly requested; prefer sandboxed or review-requesting modes for routine work. <br>
Risk: Installation examples include remote installer commands. <br>
Mitigation: Use official Antigravity CLI documentation, review installer commands before running them, and avoid remote install commands on untrusted systems. <br>


## Reference(s): <br>
- [CLI Usage](references/cli-usage.md) <br>
- [Overview and Workflows](references/overview-workflows.md) <br>
- [Interactive TUI](references/tui.md) <br>
- [Artifact Review](references/artifacts.md) <br>
- [Security and Permissions](references/security-permissions.md) <br>
- [Configuration and Platform](references/config-platform.md) <br>
- [Antigravity CLI installation](https://antigravity.google/docs/cli-install) <br>
- [Antigravity CLI overview](https://antigravity.google/docs/cli-overview) <br>
- [Antigravity CLI reference](https://antigravity.google/docs/cli-reference) <br>
- [Antigravity CLI permissions](https://antigravity.google/docs/cli-permissions) <br>
- [Antigravity CLI sandbox](https://antigravity.google/docs/cli-sandbox) <br>
- [Migrating from Gemini CLI](https://antigravity.google/docs/gcli-migration) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local `agy` help output, settings files, and artifact-review steps when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
