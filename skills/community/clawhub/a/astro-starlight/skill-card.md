## Description: <br>
Helps agents create, configure, customize, deploy, and troubleshoot Astro Starlight documentation sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[encryptshawn](https://clawhub.ai/user/encryptshawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold Astro Starlight documentation sites, configure content structure and sidebar navigation, apply styling and MDX components, prepare search and deployment, and diagnose common build or routing issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Troubleshooting snippets may remove local generated artifacts or dependency directories if copied without review. <br>
Mitigation: Confirm the project root and inspect cleanup commands before removing node_modules, package-lock.json, .astro, or dist. <br>
Risk: Process-management snippets may stop the wrong local process if copied blindly. <br>
Mitigation: Inspect the process using the target port before killing it, or run the development server on a different port. <br>
Risk: Optional analytics, search, authentication, or hosting integrations may introduce external services into a documentation site. <br>
Mitigation: Review each optional integration and confirm it matches the site's privacy, security, and deployment requirements before adding it. <br>


## Reference(s): <br>
- [Astro Starlight documentation](https://starlight.astro.build) <br>
- [Astro Starlight GitHub repository](https://github.com/withastro/starlight) <br>
- [Starlight configuration reference](https://starlight.astro.build/reference/configuration/) <br>
- [Starlight frontmatter reference](https://starlight.astro.build/reference/frontmatter/) <br>
- [Starlight components guide](https://starlight.astro.build/components/using-components/) <br>
- [Starlight community plugins](https://starlight.astro.build/resources/plugins/) <br>
- [Astro deployment guide](https://docs.astro.build/en/guides/deploy/) <br>
- [Project Setup & Structure](references/project-setup.md) <br>
- [Sidebar Navigation & Content Authoring](references/sidebar-and-content.md) <br>
- [Styling & Theming](references/styling-and-theming.md) <br>
- [Components](references/components.md) <br>
- [Deployment & Advanced Topics](references/deployment-and-advanced.md) <br>
- [Troubleshooting Starlight](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Astro, Starlight, MDX, CSS, and deployment configuration snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
