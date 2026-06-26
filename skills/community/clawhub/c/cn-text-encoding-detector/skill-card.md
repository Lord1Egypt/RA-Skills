## Description: <br>
Detect text file encoding (UTF-8, GBK, Latin-1, etc), including BOM markers, using only the Python standard library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect local text files, identify encodings such as UTF-8, UTF-16, GBK, or unknown, and decide how to process or convert those files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The detector reads the local file path supplied by the user, which could expose unintended file contents if run on the wrong path. <br>
Mitigation: Run it only on files intentionally selected for encoding inspection and avoid passing sensitive paths unless the contents are approved for local analysis. <br>
Risk: The README includes external promotional links that are outside the runtime behavior of the skill. <br>
Mitigation: Treat those links as optional external resources and evaluate them separately from the local encoding detector before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-text-encoding-detector) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runtime script prints JSON containing the input file path, detected encoding, and file size.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
