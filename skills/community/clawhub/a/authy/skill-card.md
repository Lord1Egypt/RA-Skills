## Description: <br>
Inject secrets into subprocesses via environment variables. You never see secret values - authy run injects them directly. Use for any command that needs API keys, credentials, or tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eric8810](https://clawhub.ai/user/eric8810) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use Authy to run selected commands that need API keys, credentials, or tokens without directly viewing secret values. The skill focuses on listing secret names and injecting scoped secrets into subprocess environment variables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run user-selected subprocesses with scoped secrets injected into environment variables. <br>
Mitigation: Install only when the authy binary is trusted, use narrow policies, review wrapped commands before execution, and prevent subprocesses from printing, logging, or writing secret environment variables. <br>


## Reference(s): <br>
- [Authy Command Reference](references/commands.md) <br>
- [Authy project homepage](https://github.com/eric8810/authy) <br>
- [Authy on ClawHub](https://clawhub.ai/eric8810/authy) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require the authy binary on PATH plus AUTHY_TOKEN and AUTHY_KEYFILE.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
