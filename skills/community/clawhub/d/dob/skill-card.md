## Description: <br>
Provides a Deep Memory workflow for maintaining a structured, long-term workspace knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qshfu](https://clawhub.ai/user/qshfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to look up, add, and maintain structured long-term workspace notes for libraries, tools, and technical knowledge before falling back to web search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory may capture workspace knowledge without clear consent. <br>
Mitigation: Require explicit confirmation before saving and review new or modified memory entries. <br>
Risk: Stored memory may include secrets or confidential material. <br>
Mitigation: Do not store secrets or confidential content; review memory files before relying on them. <br>
Risk: Referenced setup scripts may create workspace files. <br>
Mitigation: Inspect setup scripts before running them and confirm the intended file changes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update workspace memory files such as DEEP-MEMORY.md and deep-memory/*.md.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
