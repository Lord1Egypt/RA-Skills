## Description: <br>
CXM Neural Memory helps agents understand codebase architecture, run semantic searches across files, map dependencies before refactoring, and ingest documentation into local context memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Joeavaib](https://clawhub.ai/user/Joeavaib) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to let coding agents search local code semantically, map dependencies before changes, and collect architecture context from source files and documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local project files and may collect shell, Git, Gemini CLI, and Claude Code CLI context into persistent local storage. <br>
Mitigation: Run it only in an isolated workspace you are comfortable indexing, avoid sensitive repositories, and clear or review the ~/.cxm data directory after use. <br>
Risk: Installation can bring broad dependencies and first-run model downloads. <br>
Mitigation: Use a dedicated virtual environment, prefer the narrower pyproject dependencies unless the requirements file has been audited, and allow model downloads only from approved environments. <br>
Risk: The patching workflow can write files, and the artifact defaults allow writes when allowed_write_paths is not configured. <br>
Mitigation: Configure .cxm.yaml with narrow allowed_write_paths and patching mode set to ask_first or false before enabling any file modification workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Joeavaib/cxm-neural-memory) <br>
- [CXM Neural Memory Skill](docs/cxm-neural-memory/SKILL.md) <br>
- [CXM README Skill Guide](docs/README_SKILL.md) <br>
- [CXM Agent Skill Schema](docs/agent_skill.json) <br>
- [CXM Agent Skill Documentation](docs/agent_skill.md) <br>
- [CXM CLI Reference](docs/cli-reference.md) <br>
- [CXM Installation Guide](docs/install.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-oriented CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-mode commands are intended to return strict JSON; harvest output may also produce structured context blocks for downstream agents.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub server release evidence; artifact pyproject.toml reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
