## Description: <br>
Generate CSS Flexbox layouts using interactive CLI commands for responsive flex containers, rows, columns, and alignment configurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use Flex to create, adjust, save, and export CSS Flexbox layouts from a local command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Bash/Python script that creates and updates layout data on disk. <br>
Mitigation: Install only if local script execution is acceptable, and review ~/.flex/data.jsonl before relying on saved layouts. <br>
Risk: Export can write or overwrite a CSS file at the path selected by the user. <br>
Mitigation: Choose safe output paths and avoid storing secrets or sensitive names in layout labels. <br>


## Reference(s): <br>
- [Flex on ClawHub](https://clawhub.ai/bytesagain1/flex) <br>
- [BytesAgain](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration] <br>
**Output Format:** [CLI text output and CSS code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local JSONL layout data at ~/.flex/data.jsonl; export can write CSS to a user-selected path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
