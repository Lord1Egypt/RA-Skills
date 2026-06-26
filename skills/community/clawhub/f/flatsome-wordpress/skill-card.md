## Description: <br>
Analyzes images, URLs, or descriptions and helps recreate Flatsome theme pages with UXBuilder shortcodes, CSS, and WordPress setup guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hungphamwp](https://clawhub.ai/user/hungphamwp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and WordPress builders use this skill to analyze a reference design and generate Flatsome UXBuilder shortcode, CSS, and WP-CLI setup guidance for recreating complete pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WP-CLI guidance can mutate a real WordPress site, including plugin activation, option changes, remote media imports, and forced page deletion. <br>
Mitigation: Use a staging site first, keep a backup, and require explicit approval for the exact site, page ID, title, and command before any mutating WP-CLI action. <br>
Risk: Commands using destructive flags such as `--force` can permanently delete content. <br>
Mitigation: Do not run destructive commands unless the user has reviewed the target resource and approved the exact command. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with Flatsome UXBuilder shortcodes, CSS blocks, and inline bash/WP-CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include WordPress page IDs, image/form placeholders, and commands requiring site-specific review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
