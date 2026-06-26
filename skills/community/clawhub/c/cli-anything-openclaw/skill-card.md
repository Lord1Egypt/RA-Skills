## Description: <br>
Adapt HKUDS CLI-Anything for OpenClaw workflows. Use when the user wants to build, refine, test, or validate an agent-native CLI harness for a GUI application or source repository inside OpenClaw, mentions CLI-Anything, or asks to apply the CLI-Anything methodology on a local path or GitHub repo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[barrontang](https://clawhub.ai/user/barrontang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill in OpenClaw to analyze a local path or GitHub repository, then build, refine, test, or validate an agent-native CLI harness for a GUI application or source repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to clone repositories, install packages, run tests, invoke real application backends, and create or modify harness files in a selected codebase. <br>
Mitigation: Use a version-controlled workspace, confirm clone, pip install, pytest, and backend execution commands before running them, and review generated files plus TEST.md or session state before keeping changes. <br>


## Reference(s): <br>
- [Agent Harness: GUI-to-CLI for Open Source Software](artifact/references/harness.md) <br>
- [CLI-Anything for Codex](artifact/references/codex-skill.md) <br>
- [cli-anything Command](artifact/references/cli-anything.md) <br>
- [cli-anything-refine Command](artifact/references/cli-anything-refine.md) <br>
- [cli-anything-test Command](artifact/references/cli-anything-test.md) <br>
- [cli-anything-validate Command](artifact/references/cli-anything-validate.md) <br>
- [cli-anything-list Command](artifact/references/cli-anything-list.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, structured reports, and generated or modified project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or create an agent-harness directory, tests, TEST.md, setup.py packaging, and CLI entry points in the selected workspace.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
