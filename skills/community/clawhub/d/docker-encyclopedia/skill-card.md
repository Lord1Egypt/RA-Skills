## Description: <br>
Docker documentation-first workflow for Docker-specific questions, troubleshooting, command planning, image/build work, container/runtime operations, Compose behavior, networking, volumes, registries, and diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kklouzal](https://clawhub.ai/user/kklouzal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to answer Docker-specific questions, plan Docker commands, troubleshoot build/runtime behavior, and maintain a workspace-local cache of consulted official Docker documentation and operational notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may write Docker environment details into workspace-local cache, note, or inventory files. <br>
Mitigation: Review or disable note-taking for sensitive environments and keep credentials, tokens, private URLs, and other secrets out of .Docker-Encyclopedia/. <br>
Risk: Docker command guidance can affect running containers, images, volumes, networks, registries, credentials, or host reachability if executed without review. <br>
Mitigation: Consult official Docker documentation, inspect current environment state first, and review high-impact commands before execution. <br>


## Reference(s): <br>
- [Docker Documentation](https://docs.docker.com/) <br>
- [Docker Encyclopedia Skill Page](https://clawhub.ai/kklouzal/docker-encyclopedia) <br>
- [Workflow](references/workflow.md) <br>
- [Cache Layout](references/cache-layout.md) <br>
- [Topic Map](references/topic-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and workspace note files when caching or recording Docker knowledge] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch official Docker documentation and write cached documentation, notes, and inventory files under .Docker-Encyclopedia/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
