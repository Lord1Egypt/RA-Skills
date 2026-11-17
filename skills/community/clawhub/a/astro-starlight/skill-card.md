## Description:

Helps agents create, configure, customize, deploy, and troubleshoot Astro Starlight documentation sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to scaffold and maintain Astro Starlight documentation sites, including sidebar structure, content authoring, MDX components, theming, search, deployment, i18n, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package-manager and setup commands can change a project or install dependencies in the wrong location.

Mitigation: Run commands only from the intended project directory and consider pinning package versions for reproducible builds.

Risk: Troubleshooting cleanup commands can remove local dependencies, lockfiles, build output, or generated type caches.

Mitigation: Verify the current directory and command target before running cleanup commands such as rm -rf.

Risk: Commands that inspect or stop local processes can interrupt unrelated development work.

Mitigation: Inspect matching processes and ports before killing anything.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/encryptshawn/skills/astro-starlight)
- [Project setup reference](references/project-setup.md)
- [Sidebar and content reference](references/sidebar-and-content.md)
- [Styling and theming reference](references/styling-and-theming.md)
- [Components reference](references/components.md)
- [Deployment and advanced topics reference](references/deployment-and-advanced.md)
- [Troubleshooting reference](references/troubleshooting.md)
- [Astro Starlight documentation](https://starlight.astro.build)
- [Astro Starlight GitHub repository](https://github.com/withastro/starlight)
- [Astro deployment guide](https://docs.astro.build/en/guides/deploy/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project structure, Astro/Starlight configuration, MDX examples, deployment checks, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
