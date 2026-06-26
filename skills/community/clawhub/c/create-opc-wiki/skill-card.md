## Description: <br>
Scaffold a personal LLM wiki with multi-agent rules, MCP support, privacy-tagged markdown, and an optional static publishing target. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mackding](https://clawhub.ai/user/mackding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create a local personal-knowledge-base vault, then ingest sources, query compiled wiki pages, lint stale or contradictory notes, expose selected pages through MCP, and optionally publish public pages as a static site. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs the agent to run an external npm scaffolder that creates local files and agent configuration. <br>
Mitigation: Install only if you trust the create-opc-wiki npm package and repository, use a dedicated vault folder, and review generated files before relying on them. <br>
Risk: Generated agent rules and MCP files can affect how connected agents access and summarize wiki content. <br>
Mitigation: Review generated agent rules and MCP files before opening the vault in agents or MCP clients. <br>
Risk: Publishing the optional static site can expose notes tagged as public. <br>
Mitigation: Do not tag secrets, personal notes, or confidential material as privacy: public before building or deploying the site. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mackding/create-opc-wiki) <br>
- [create-opc-wiki npm package](https://www.npmjs.com/package/create-opc-wiki) <br>
- [LLM Wiki inspiration](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce machine-readable JSON output when the scaffolder is run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
