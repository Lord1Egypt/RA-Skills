## Description: <br>
Auto-generates a CLI reference doc so your agent stops guessing OpenClaw commands and starts working. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dank-varley](https://clawhub.ai/user/dank-varley) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate a local OpenClaw CLI reference for the installed OpenClaw version, including commands, subcommands, flags, JSON support, and optional documentation links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script invokes the locally installed OpenClaw CLI and writes generated reference files under ~/.openclaw by default. <br>
Mitigation: Review the script before execution and use --output=PATH when you want the generated file written somewhere other than the default OpenClaw workspace notes directory. <br>
Risk: Enrich mode can fetch documentation from docs.openclaw.ai and incorporate retrieved material into the generated note. <br>
Mitigation: Use local-only mode when network access is not desired, and review enriched output before relying on it. <br>
Risk: Non-interactive mode can overwrite an existing openclaw-cli-reference.md file. <br>
Mitigation: Back up the existing reference or run without --yes to choose whether to overwrite, keep both versions, or cancel. <br>


## Reference(s): <br>
- [OpenClaw Boot Camp release page](https://clawhub.ai/dank-varley/bootcamp) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown file with CLI reference content and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the generated reference to the OpenClaw workspace notes directory by default; optional enrich mode adds documentation links.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
