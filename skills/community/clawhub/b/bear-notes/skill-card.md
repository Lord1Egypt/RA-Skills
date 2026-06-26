## Description: <br>
Create, search, and manage Bear notes via grizzly CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Bear users can use this skill to have an agent create, read, append to, tag, and search Bear notes on macOS through the grizzly CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bear tokens can expose access to private notes if stored or shared carelessly. <br>
Mitigation: Store the token as a secret, restrict token file permissions, and avoid placing real tokens in shell history. <br>
Risk: Some commands can read or modify private Bear notes. <br>
Mitigation: Review commands before execution and use --dry-run or --print-url when previewing actions matters. <br>


## Reference(s): <br>
- [Bear](https://bear.app) <br>
- [grizzly CLI module](https://github.com/tylerwince/grizzly) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and TOML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Bear callback JSON when commands are run with callbacks enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
