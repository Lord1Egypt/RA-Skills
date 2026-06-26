## Description: <br>
Fetch and install C++ tools/libraries from cpp_tools repository for downloading, cloning, building, installing, listing, and managing repository URLs for third-party C++ libraries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyendt](https://clawhub.ai/user/wangyendt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to have an agent propose gettool commands for fetching C++ library sources, optionally building them with CMake/make, running configured installation scripts, and managing the cpp_tools repository URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to fetch, build, and install third-party code, including system-wide installation with sudo. <br>
Mitigation: Confirm the repository URL, package name, target path, exact command, and install scope before execution; prefer project-local directories, pinned versions, and inspection of build or install scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyendt/gettool) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may include local paths, version or branch selectors, repository URL changes, build flags, and install flags.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
