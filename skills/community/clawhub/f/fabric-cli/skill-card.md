## Description: <br>
Helps agents use Fabric.so's `fabric` CLI for setup checks, workspace search, saving notes, links, and files, task management, assistant queries, shell completion, JSON workflows, and persistent agent memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to operate the Fabric.so CLI from a shell, including searching or browsing a Fabric library, saving workspace content, managing tasks and workspaces, checking setup, and using Fabric as a persistent memory layer. It is intended for Fabric.so `fabric`, not Microsoft Fabric `fab` or other unrelated Fabric tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to read, write, and persist data in a remote Fabric workspace. <br>
Mitigation: Review write, upload, workspace switch, installer, authentication, and memory actions before execution; require explicit confirmation for destructive or hard-to-reverse operations. <br>
Risk: Fabric memory and file uploads may expose secrets or sensitive personal data if used carelessly. <br>
Mitigation: Do not store secrets, credential files, private keys, browser profiles, raw transcripts, or sensitive personal data in Fabric; redact tokens and prefer secure authentication routes. <br>


## Reference(s): <br>
- [Fabric User Guide: CLI usage](https://user-guide.fabric.so/ai-tools/CLI-usage) <br>
- [Fabric CLI download page](https://fabric.so/download/cli) <br>
- [Sources and provenance](references/sources.md) <br>
- [Command reference](references/command-reference.md) <br>
- [Workflow playbook](references/workflows.md) <br>
- [Security and consent guide](references/security-and-consent.md) <br>
- [Agent memory guide](references/agent-memory.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, JSON, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands, JSON command plans, and structured note templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live CLI help checks when syntax may vary and prefers JSON output for parseable Fabric CLI responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata version: 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
