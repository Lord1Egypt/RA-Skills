## Description: <br>
Searches and explores Are.na for curated channels, references, visual inspiration, linked resources, and key curators across research topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[givenness](https://clawhub.ai/user/givenness) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, designers, writers, and agents use this skill to search Are.na, inspect curated collections, follow channel and block connections, identify recurring curators, and synthesize sourced research briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed package documents running Are.na helper code, but the helper CLI files are not included in the artifact. <br>
Mitigation: Review or supply the missing CLI code before installation and execution. <br>
Risk: The skill asks users to source a broad local environment file that may expose unrelated secrets. <br>
Mitigation: Use only a scoped ARENA_ACCESS_TOKEN for this skill instead of sourcing a global environment file. <br>
Risk: Authenticated Are.na scopes may allow access to personal collections through my or following searches. <br>
Mitigation: Avoid authenticated scopes unless the user explicitly wants the agent to access personal Are.na collections. <br>


## Reference(s): <br>
- [Arena Research on ClawHub](https://clawhub.ai/givenness/arena-research-skill) <br>
- [givenness publisher profile](https://clawhub.ai/user/givenness) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON output from the Are.na CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save sourced research briefs to local markdown drafts when the documented --save option is used.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
