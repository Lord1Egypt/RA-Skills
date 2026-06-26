## Description: <br>
Cargo routes agents across the Cargo CLI skill bundle, explaining capability selection, UUID flow, async polling, end-to-end GTM workflows, and common CLI pitfalls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cargo-ai](https://clawhub.ai/user/cargo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and GTM operators use Cargo to choose and chain Cargo CLI skills for workspace setup, enrichment, CRM sync, AI lead scoring, workflow monitoring, segment export, and GTM context authoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cargo CLI access can affect the active Cargo workspace. <br>
Mitigation: Authenticate with OAuth when possible, confirm the active workspace before writes, and use workspace-scoped tokens stored in a secrets manager for non-interactive use. <br>
Risk: Optional installer hooks can refresh skills and checkpoint Cargo session rows. <br>
Mitigation: Review installer hooks and default-branch context updates before enabling them in a workspace. <br>
Risk: Some Cargo commands require elevated workspace permissions. <br>
Mitigation: Use admin tokens only for admin-only operations and re-issue commands with the minimum workspace role that can complete the task. <br>


## Reference(s): <br>
- [Cargo Skill on ClawHub](https://clawhub.ai/cargo-ai/cargo) <br>
- [Cargo Skills Repository](https://github.com/getcargohq/cargo-skills) <br>
- [Prerequisites](references/prerequisites.md) <br>
- [End-to-end use cases](references/use-cases.md) <br>
- [UUID flow](references/uuid-flow.md) <br>
- [Glossary](references/glossary.md) <br>
- [Common gotchas](references/gotchas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cargo CLI commands generally return JSON on stdout; async operations may require polling or wait flags.] <br>

## Skill Version(s): <br>
1.5.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
