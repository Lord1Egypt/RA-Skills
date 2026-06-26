## Description: <br>
Scrapes airline aircraft seatmap data, organizes related images, and generates structured website-ready airline and aircraft documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxinyu123](https://clawhub.ai/user/wangxinyu123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to collect airline aircraft information from seatmaps.com, classify downloaded images, deduplicate assets, and prepare Markdown data for a website. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documentation recommends broad permission-bypass execution and persistent Claude permission changes. <br>
Mitigation: Run it only in a dedicated project folder, avoid permission-bypass startup and persistent global settings, and grant only the minimum file access needed for the selected output directory. <br>
Risk: The deduplication workflow can delete duplicate image files. <br>
Mitigation: Run deduplication with --dry-run first, review the report, and keep backups or version control for generated image directories before allowing deletions. <br>
Risk: The scraper fetches third-party seatmap data and images from seatmaps.com. <br>
Mitigation: Confirm that the intended use complies with the source site's terms and review generated content before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangxinyu123/airline-info-to-website) <br>
- [Publisher profile](https://clawhub.ai/user/wangxinyu123) <br>
- [Reference manual](references/reference.md) <br>
- [Examples](references/examples.md) <br>
- [Aircraft detail template](references/template.md) <br>
- [Scripts README](scripts/README.md) <br>
- [seatmaps.com airline index](https://seatmaps.com/zh-CN/airlines/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation, image directories, classification reports, and command-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes scraped aircraft data under FlightData/ by default and may delete duplicate images when deduplication is run without --dry-run.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
