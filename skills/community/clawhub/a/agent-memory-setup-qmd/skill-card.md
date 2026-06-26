## Description: <br>
Set up the full OpenClaw agent memory system with 3-tier memory, daily logs, semantic search with QMD, and lossless context management with Lossless Claw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autosolutionsai-didac](https://clawhub.ai/user/autosolutionsai-didac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to initialize persistent memory for OpenClaw agents, including memory files, daily logs, semantic search guidance, and OpenClaw configuration steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent agent memory that future agents may read. <br>
Mitigation: Install it only in workspaces intended for long-term memory and avoid storing secrets, credentials, regulated data, or private personal details unless future access is deliberate. <br>
Risk: The setup process depends on local tooling and may install or guide installation of QMD and Lossless Claw. <br>
Mitigation: Review the setup script and AGENTS.md template before use, and verify the Lossless Claw plugin source when supply-chain controls matter. <br>


## Reference(s): <br>
- [OpenClaw homepage](https://github.com/nichochar/openclaw) <br>
- [AGENTS template](references/AGENTS_TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance for memory files, OpenClaw configuration, and verification steps.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
