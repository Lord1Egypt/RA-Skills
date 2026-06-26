## Description: <br>
Build and query AST summaries + call graphs for codebases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sg345662365-oss](https://clawhub.ai/user/sg345662365-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use CodeGraph to build a local structural cache for a project and query functions, classes, imports, file summaries, callers, and calls before reading or editing source files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local cache can summarize file names, function and class names, imports, calls, line numbers, and the project path from sensitive repositories. <br>
Mitigation: Use --exclude or --output when scanning sensitive repositories, and review the generated .code-graph.json before sharing it. <br>
Risk: Static AST and regex-based summaries can miss dynamic behavior or produce incomplete call relationships. <br>
Mitigation: Use the output as a navigation aid and confirm important findings against source code and tests before making changes. <br>


## Reference(s): <br>
- [CodeGraph ClawHub release](https://clawhub.ai/sg345662365-oss/codegraph) <br>
- [sg345662365-oss ClawHub publisher profile](https://clawhub.ai/user/sg345662365-oss) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON cache/query output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or queries a local .code-graph.json cache unless an alternate output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
