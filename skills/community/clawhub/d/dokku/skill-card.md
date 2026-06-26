## Description: <br>
Installs, upgrades, and manages Dokku apps, deploys code or images, runs tasks, and cleans up containers on Dokku hosts via CLI commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akhil-naidu](https://clawhub.ai/user/akhil-naidu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to administer Dokku hosts: installing or upgrading Dokku, creating and managing apps, deploying from Git or container images, running one-off or background tasks, inspecting logs, configuring domains and certificates, and cleaning up containers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose powerful root-level infrastructure actions on Dokku hosts. <br>
Mitigation: Install it only when agent-assisted Dokku administration is intended, and review every sudo command before execution. <br>
Risk: Plugin URLs, network binding changes, Docker prune commands, and background commands can affect host security, availability, or data retention. <br>
Mitigation: Review these commands before running them, prefer pinned official sources and verified scripts, and avoid generic deployment prompts unless Dokku changes are explicitly intended. <br>


## Reference(s): <br>
- [Dokku installation documentation](https://dokku.com/docs/getting-started/installation) <br>
- [Dokku upgrading documentation](https://dokku.com/docs/getting-started/upgrading) <br>
- [Dokku releases](https://github.com/dokku/dokku/releases) <br>
- [Docker prune command reference](https://docs.docker.com/engine/reference/commandline/system_prune/) <br>
- [Dokku Let's Encrypt plugin](https://github.com/dokku/dokku-letsencrypt.git) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command guidance targets Dokku hosts and may require SSH, local shell access, the dokku CLI, Docker, and sudo privileges.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence; artifact changelog lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
