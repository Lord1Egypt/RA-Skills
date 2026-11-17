## Description:

This skill helps agents collect airline aircraft and seat-map data from seatmaps.com, classify downloaded images, remove duplicate images, and create Markdown content for website display.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxinyu123](https://clawhub.ai/user/wangxinyu123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to gather aircraft seat-map data, organize related images, and produce structured Markdown assets for airline information websites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact asks users to bypass agent permissions and grant broad shell and file-write access.

Mitigation: Run the skill only in a constrained project directory and do not use permission bypass or broad persistent settings.

Risk: The scraper downloads external content and writes generated files into the selected output directory.

Mitigation: Use dry-run and limit options first, confirm the target output path, and restrict scraping to trusted seatmaps.com URLs.

Risk: The deduplication script can delete duplicate image files when not run in dry-run mode.

Mitigation: Back up downloaded data and run deduplication with --dry-run before allowing file deletion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxinyu123/skills/airline-info-to-website)
- [Reference manual](references/reference.md)
- [Examples](references/examples.md)
- [Scripts README](scripts/README.md)
- [Seatmaps airline directory](https://seatmaps.com/zh-CN/airlines/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces airline data folders, downloaded image assets, Markdown aircraft detail files, and classification or deduplication reports.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
