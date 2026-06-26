## Description: <br>
Development skill for bili-rs, a Rust CLI tool for Bilibili, used when implementing features, fixing bugs, or extending the bilibili-cli-rust codebase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18621063286](https://clawhub.ai/user/18621063286) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to work on a Rust Bilibili CLI by following its layered architecture, command patterns, API conventions, authentication requirements, and output formatting rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill discusses account credentials and authenticated Bilibili operations. <br>
Mitigation: Keep SESSDATA and bili_jct out of logs, examples, and generated code unless explicitly required and approved by the user. <br>
Risk: The skill can guide changes that post, delete, spend coins, unfollow, or otherwise modify a Bilibili account. <br>
Mitigation: Require explicit user approval before running commands or implementing changes that perform account-mutating actions. <br>


## Reference(s): <br>
- [Bili Rs ClawHub release](https://clawhub.ai/18621063286/bili-rs) <br>
- [Bilibili API endpoints and payloads](references/api.md) <br>
- [Bili Rs CLI commands reference](references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, command examples, and structured implementation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose source changes, quality-gate commands, API request patterns, and credential-handling guidance for the bili-rs project.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
