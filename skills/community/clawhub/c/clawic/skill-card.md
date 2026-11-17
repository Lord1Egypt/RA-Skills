## Description:

Search, inspect, and install Clawic skills from GitHub with local lexical matching, registry overrides, and safe destination control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose the right Clawic CLI commands for searching, inspecting, and installing skills while keeping runtime, registry, destination, and overwrite choices explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI package or selected registry may be untrusted or change over time.

Mitigation: Install only from trusted package and registry sources; prefer pinned or project-local workflows when repeatability matters.

Risk: Running install writes downloaded skill files into the chosen destination and may overwrite files when force behavior is selected.

Mitigation: Run show before install when reviewing a skill, choose a deliberate destination directory, inspect existing files, and use --force only for intentional replacement.

Risk: Registry and manifest fetches disclose standard HTTP requests to the active registry host.

Mitigation: Keep the default registry unless an alternate compatible registry is intentional, and review the active base URL before use.

## Reference(s):

- [Clawic skill page](https://clawhub.ai/ivangdavila/skills/clawic)
- [Clawic homepage](https://clawic.com/skills/clawic)
- [Default Clawic registry index](https://raw.githubusercontent.com/clawic/skills/main/registry/index.json)
- [Registry and manifests evidence](artifact/registry-and-manifests.md)
- [Install safety evidence](artifact/install-safety.md)
- [Command patterns evidence](artifact/command-patterns.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command sequences, registry checks, install destination guidance, and overwrite cautions.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
