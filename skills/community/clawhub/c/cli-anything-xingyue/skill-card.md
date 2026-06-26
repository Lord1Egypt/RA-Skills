## Description: <br>
Cli Anything helps agents generate, install, refine, and validate command-line interfaces for existing software so those tools can be controlled through shell commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YIKAI123456](https://clawhub.ai/user/YIKAI123456) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install prebuilt CLI harnesses or guide CLI generation for software such as GIMP, Blender, LibreOffice, and OBS so an agent can invoke those tools through shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch changing GitHub code and update CLI-Anything content under the user's home directory. <br>
Mitigation: Install only when the upstream CLI-Anything repository is trusted, review fetched code before use, and prefer an isolated workspace for evaluation. <br>
Risk: The skill can install generated or upstream Python harness packages into the user's environment with pip. <br>
Mitigation: Review harness contents before /cli-install, use a virtual environment or container, and uninstall generated packages when no longer needed. <br>
Risk: Generated CLIs may act on local software, files, or project repositories. <br>
Mitigation: Avoid running the skill on untrusted repositories and review generated commands and outputs before applying them to important files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/YIKAI123456/cli-anything-xingyue) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/YIKAI123456) <br>
- [CLI-Anything Project Referenced by Skill](https://github.com/HKUDS/CLI-Anything) <br>
- [CLI-Anything Documentation Referenced by Skill](https://github.com/HKUDS/CLI-Anything/blob/main/README_CN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide or invoke git and pip workflows, and may generate or install CLI harness files in the user's environment.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
