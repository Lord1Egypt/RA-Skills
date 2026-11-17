# Project Manager runtime

An OpenClaw skill for engineering project control: guided setup, bounded agent
delegation, revisioned requirements, traceability, changes, baselines, verification
evidence, risks, problems, milestones and release gates.

Read [SKILL.md](SKILL.md) for the agent workflow. The full installation guide,
demonstration, contribution tools and changelog are in the
[source repository](https://github.com/aminekhettat/engineering-project-manager).

## Requirements and use

Linux (including Raspberry Pi OS), Python 3.10+ and Git. There are no Python
package dependencies. Windows users need Linux/WSL; native Windows is unsupported.
GitHub bootstrap requires authenticated `gh`; GitLab bootstrap requires
authenticated `glab`. SSH remotes require a configured SSH client and identity.

Install this entire directory as `project-manager` inside your OpenClaw skills
directory. Do not copy only SKILL.md. Start a fresh agent session and ask:

> Use project-manager to initialize my project. Discover existing work first,
> ask the missing scope, infrastructure and delegation questions, and show the
> resolved setup before creating infrastructure.

For existing projects, request a read-only status and migration assessment.
Run CLI commands from this skill directory and pass the absolute project path.
Contributor tests live in the source repository, not this runtime package.

## Scope and license

**SPICE-like, not certified.** This independent tool is not certified, endorsed
or approved by ISO, VDA QMC or iNTACS. Passing its checks does not establish
conformity, a capability level, safety or regulatory compliance. See
[SPICE scope](docs/SPICE-SCOPE.md) and [security guidance](SECURITY.md).
The license of this distribution is in [LICENSE](LICENSE). Third-party standards
and project inputs retain their own terms.
