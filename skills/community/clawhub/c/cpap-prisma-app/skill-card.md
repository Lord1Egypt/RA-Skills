## Description: <br>
Fetches CPAP therapy data from the PrismaAPP API and writes a daily Obsidian log note. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanwebgit](https://clawhub.ai/user/sanwebgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with a PrismaAPP account and compatible CPAP device use this skill to fetch daily or historical therapy data and save structured Obsidian health notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses locally stored PrismaAPP credentials to access personal CPAP health data. <br>
Mitigation: Protect config.json, keep it out of sync and source control, and install only when comfortable storing PrismaAPP credentials locally. <br>
Risk: Generated CPAP notes may expose sensitive health information in an Obsidian vault, including cloud-synced or shared vaults. <br>
Mitigation: Verify vault_path and log_dir before running, and review vault sync and sharing settings before saving backfilled data. <br>
Risk: Backfill modes can write many dated Markdown notes to the configured log directory. <br>
Mitigation: Confirm the date range and destination directory before using --all or --from. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sanwebgit/cpap-prisma-app) <br>
- [PrismaAPP API Base](https://my.prismacloud.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown files with YAML frontmatter, localized note sections, and console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes one Obsidian note per requested date under the configured vault path and log directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
