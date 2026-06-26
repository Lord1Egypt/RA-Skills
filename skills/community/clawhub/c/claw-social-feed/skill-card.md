## Description: <br>
Fetches social media timelines from supported platforms and saves filtered, tagged Markdown files into an Obsidian vault. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glassmarbles](https://clawhub.ai/user/glassmarbles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure account-based social content collection, run incremental syncs, and save selected posts as Obsidian Markdown notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use logged-in browser sessions through bb-browser. <br>
Mitigation: Configure only the specific accounts and platforms needed, avoid bookmarks or notifications unless explicitly required, and review scope before running. <br>
Risk: The skill writes fetched content into an Obsidian vault. <br>
Mitigation: Run with dry-run first, confirm the configured vault path, and inspect generated notes before enabling routine use. <br>
Risk: Scheduled sync can create recurring jobs. <br>
Mitigation: Inspect any cron entry before enabling it and keep clear instructions for disabling the schedule. <br>


## Reference(s): <br>
- [Supported Platforms](references/platforms.md) <br>
- [bb-sites](https://github.com/epiral/bb-sites) <br>
- [ClawHub Skill Page](https://clawhub.ai/glassmarbles/claw-social-feed) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples; generated vault content is Markdown files with YAML frontmatter.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local state and Obsidian Markdown files when the user runs the bundled script.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
