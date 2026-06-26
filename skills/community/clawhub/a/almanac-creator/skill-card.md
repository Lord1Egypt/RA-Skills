## Description: <br>
Almanac Creator generates traditional Chinese Huangli calendar PNG images with zodiac fortune, fengshui timing, auspicious activities, and styling guidance for social media publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangj85](https://clawhub.ai/user/zhangj85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, social media operators, and developers use this skill to generate one-day or batch Chinese almanac image sets for Toutiao, Douyin, Xiaohongshu, or similar publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated date-named PNG files may overwrite existing outputs in the selected folder. <br>
Mitigation: Use a dedicated output directory for each run or review existing files before enabling overwrite behavior. <br>
Risk: Optional examples can make third-party almanac API requests or run the generator on a recurring schedule. <br>
Mitigation: Use optional API or scheduled-task workflows only after reviewing the network request, data-sharing expectations, and local recurrence settings. <br>
Risk: Traditional almanac, zodiac, fengshui, and fortune content may be misleading if treated as factual decision support. <br>
Mitigation: Review generated content before publishing and retain the traditional-culture, reference-only disclaimer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangj85/almanac-creator) <br>
- [Almanac image standard](references/almanac-image-standard.md) <br>
- [lunar-python API guide](references/lunar-python-api-guide.md) <br>
- [Usage examples](references/usage-examples.md) <br>
- [Qingyunke almanac API](https://api.qingyunke.com/api.php) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, configuration, guidance] <br>
**Output Format:** [PNG image files plus Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates one to three 1080x1400 PNG pages per date; batch mode can create date-grouped output directories.] <br>

## Skill Version(s): <br>
3.0.5 (source: release evidence; artifact frontmatter reports 3.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
