## Description: <br>
Cn Diff Checker compares two text strings or local files and shows line-, word-, or character-level differences using Python's standard difflib output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and reviewers use this skill to compare text snippets or explicitly provided local files from an agent session and inspect changes at line, word, or character granularity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool reads any local file path explicitly passed to it, and diff output may display sensitive file contents in the terminal or redirected output. <br>
Mitigation: Avoid comparing sensitive files unless their contents are intended to be viewed or captured in the agent session output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-diff-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text with ANSI-colored diff output and optional file redirection guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads only text strings or file paths explicitly provided by the user; no network output.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
