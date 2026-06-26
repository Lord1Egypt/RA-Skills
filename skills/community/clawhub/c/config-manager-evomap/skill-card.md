## Description: <br>
Config Manager - Evomap Asset provides a type-safe C library for dynamic key-value configuration management with string, integer, boolean, and file-backed configuration support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gatsby047-oss](https://clawhub.ai/user/gatsby047-oss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers can use this skill when converting hard-coded C settings into dynamic key-value configuration. It is suited for local utilities or applications that need typed accessors, defaults, and simple key=value file load/save support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saving configuration uses normal overwrite behavior for the file path supplied by the caller. <br>
Mitigation: Review and constrain load/save paths before use, and avoid passing important files unless overwrite is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gatsby047-oss/config-manager-evomap) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with C code examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local C configuration helper code and usage guidance; no network service output is described.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
