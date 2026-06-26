## Description: <br>
Converts natural language descriptions into structured outputs such as SQL queries, JSON objects, API request specifications, search queries, regex patterns, schemas, and shell commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn plain-language requests into machine-readable structures while preserving intent, constraints, and assumptions for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security verdict is suspicious because install metadata and documentation overstate sensitive capabilities and leave credential or write behavior unclear. <br>
Mitigation: Review before installing and do not grant financial, purchase, OAuth, or sensitive-credential access unless the publisher narrows and explains those requirements. <br>
Risk: Generated SQL, API calls, and shell commands can be incorrect or unsafe if treated as executable instructions. <br>
Mitigation: Treat generated outputs as untrusted drafts, validate them against the target system, and require explicit review before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjipeng977/convert-natural-language) <br>
- [Publisher profile](https://clawhub.ai/user/wangjipeng977) <br>
- [Metadata source repository](https://github.com/MiniMax-AI/skills) <br>
- [Reference index](references/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or structured snippets with explanations, confidence notes, warnings, and assumptions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SQL, JSON, HTTP request specifications, search queries, regex patterns, schemas, or CLI commands depending on the requested conversion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact changelog lists 1.0 released 2026-05-21) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
