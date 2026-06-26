## Description: <br>
Provides a standard protocol for delegating tasks through the ACP runtime to acpx-enabled harnesses such as Claude Code and Codex. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoyang78](https://clawhub.ai/user/chaoyang78) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coordinator agents use this skill to delegate work to ACP-compatible harnesses while preserving session threading, authentication checks, and troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated harnesses may act without approval prompts when configured with global approve-all permissions. <br>
Mitigation: Prefer read-only or per-action approval, restrict the working directory, and avoid global approve-all for routine use. <br>
Risk: Provider credentials may be exposed or misused if stored insecurely in acpx configuration. <br>
Mitigation: Protect ~/.acpx/config.json and API keys, and install only when the delegated ACP harnesses are trusted. <br>


## Reference(s): <br>
- [Harness List](references/harness-list.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/chaoyang78/acp-harness-delegation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance; does not itself execute delegated harness calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
