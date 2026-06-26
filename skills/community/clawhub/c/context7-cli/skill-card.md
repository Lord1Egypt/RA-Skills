## Description: <br>
Manage Context7 via CLI - search libraries, get documentation context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Melvynx](https://clawhub.ai/user/Melvynx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search Context7 for libraries and retrieve current documentation snippets by library, version, and query. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can run unpinned remote installer code on the user's machine. <br>
Mitigation: Review install commands before execution and prefer trusted, pinned, or manually inspected installation methods. <br>
Risk: The skill requires storing and testing a Context7 API key. <br>
Mitigation: Use a revocable Context7 API key with only the minimum access needed. <br>


## Reference(s): <br>
- [Context7 API key dashboard](https://context7.com/dashboard) <br>
- [Bun installer](https://bun.sh/install) <br>
- [ClawHub skill page](https://clawhub.ai/Melvynx/context7-cli) <br>
- [Publisher profile](https://clawhub.ai/user/Melvynx) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and CLI output formats including JSON, text, CSV, and YAML] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Programmatic CLI calls should use the --json flag; authentication uses a Context7 API key.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
