## Description: <br>
clawgrep is a grep-like CLI skill for hybrid semantic and keyword search across code, documents, and large folders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[schonhoffer](https://clawhub.ai/user/schonhoffer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use clawgrep to find relevant code or document passages when the exact wording is unknown, while keeping output compatible with grep-style parsing and scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on installing or invoking a third-party local CLI package. <br>
Mitigation: Verify that the clawgrep package or repository is the intended trusted source before installing or running it. <br>
Risk: First use downloads an ONNX embedding model and local caching can persist model data and search indexes. <br>
Mitigation: Expect the first-run download, search the narrowest practical paths, and use --no-cache or a dedicated cache directory for sensitive temporary content. <br>


## Reference(s): <br>
- [CLI Reference](references/cli-reference.md) <br>
- [Examples](references/examples.md) <br>
- [clawgrep Repository](https://github.com/Schonhoffer/clawgrep) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and grep-compatible text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are ranked by relevance and may include file paths, line numbers, context lines, counts, filenames, scores, or exit codes depending on CLI flags.] <br>

## Skill Version(s): <br>
0.1.4 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
