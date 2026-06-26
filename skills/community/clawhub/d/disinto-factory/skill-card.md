## Description: <br>
Set up and operate a disinto autonomous code factory for bootstrapping a factory instance, checking agents and CI, managing backlog work, and troubleshooting the stack. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johba37](https://clawhub.ai/user/johba37) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and engineering operators use this skill to initialize and run an autonomous code factory around repositories, local Forgejo, Woodpecker CI, containerized agents, backlog triage, pull requests, merges, mirrors, and operational troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad repository, CI, local token, Docker container, and external mirror operations. <br>
Mitigation: Run it in an isolated environment, use trusted workloads, review mirror and merge settings, and limit access to required repositories and services. <br>
Risk: Some workflows include destructive or privileged operations such as branch deletion, state cleanup, hard resets, password resets, and privileged host-network CI changes. <br>
Mitigation: Require human confirmation before destructive or privileged commands and review the exact target repository, branch, container, and credentials before execution. <br>


## Reference(s): <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Project homepage](https://disinto.ai) <br>
- [Repository](https://github.com/disinto/disinto) <br>
- [ClawHub release page](https://clawhub.ai/johba37/disinto-factory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational checklists and command sequences for local factory setup, status checks, CI inspection, mirroring, and troubleshooting.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
